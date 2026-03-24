#!/usr/bin/env python3
"""
crawl_docs.py — General documentation crawler.

Usage:
    python crawl_docs.py <index_url> [--max-pages N]

Examples:
    python crawl_docs.py https://kernc.github.io/backtesting.py/doc/backtesting/index.html
    python crawl_docs.py https://docs.python.org/3/library/index.html --max-pages 50

Outputs:
    docs/<framework-name>/
        _index.md           ← master index: file list + one-line descriptions
        <page-name>.md      ← one file per crawled page, clean markdown
"""

import argparse
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    import html2text
except ImportError:
    sys.exit(
        "Missing dependencies. Run:\n"
        "  pip install requests beautifulsoup4 html2text"
    )


# ── helpers ────────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Turn any string into a safe, readable filename stem."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "_", text)
    text = re.sub(r"^_+|_+$", "", text)
    return text or "page"


def framework_name_from(url: str, soup: BeautifulSoup) -> str:
    """
    Derive a short framework name for the output directory.
    Tries the <title> tag first, falls back to the URL path, then hostname.
    Strips common doc-noise words (api, documentation, docs, reference, etc.)
    and caps at the first 2 meaningful tokens so names stay short.
    """
    NOISE = {"api", "documentation", "docs", "doc", "reference", "manual",
             "guide", "index", "html", "package", "module", "lib", "library"}

    title_tag = soup.find("title")
    if title_tag and title_tag.get_text(strip=True):
        raw = title_tag.get_text(strip=True)
        # Split on common separators and take the first segment
        for sep in ("|", "—", "-", "·", "–"):
            raw = raw.split(sep)[0]
        tokens = [t for t in slugify(raw).split("_") if t and t not in NOISE]
        if tokens:
            name = "_".join(tokens[:2])      # max 2 tokens → "backtesting_py"
            if 2 < len(name) < 40:
                return name

    # Fall back to URL path segments
    parts = urlparse(url).path.strip("/").split("/")
    for part in parts:
        candidate = slugify(part)
        if 2 < len(candidate) < 30 and candidate not in NOISE:
            return candidate

    host = urlparse(url).hostname or "docs"
    return slugify(host.split(".")[0])


def page_filename(url: str, title: str, existing: set) -> str:
    """
    Build a unique, descriptive filename for a page.

    Strategy (in priority order):
    1. Last two meaningful URL path segments joined with "_"
       e.g. backtesting/lib.html  → "backtesting_lib"
            backtesting/index.html → "backtesting_index" (only last if unambiguous)
    2. Cleaned title slug (dots→underscores, noise words stripped)
    3. Plain "page" fallback
    """
    NOISE_FILENAMES = {"index", "html", "doc", "docs", "api", "documentation",
                       "reference", "guide", "manual"}

    parsed_path = urlparse(url).path.rstrip("/")
    parts = [p for p in parsed_path.split("/") if p]
    # Take last 2 meaningful path segments (without extension)
    segments = [slugify(Path(p).stem) for p in parts[-2:] if p]
    segments = [s for s in segments if s and s not in NOISE_FILENAMES]
    url_candidate = "_".join(segments) if segments else ""

    # Cleaned title: replace dots → underscores, then slugify, then strip noise
    clean_title = title.replace(".", "_")
    title_tokens = [t for t in slugify(clean_title).split("_")
                    if t and t not in NOISE_FILENAMES]
    title_candidate = "_".join(title_tokens[:4])  # cap at 4 tokens

    candidate = url_candidate or title_candidate or "page"

    # Avoid collisions
    final = candidate
    counter = 2
    while final in existing:
        final = f"{candidate}_{counter}"
        counter += 1

    existing.add(final)
    return final + ".md"


def html_to_markdown(html: str, base_url: str) -> str:
    """Convert raw HTML to clean Markdown."""
    converter = html2text.HTML2Text()
    converter.baseurl = base_url
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0          # no line-wrapping
    converter.protect_links = False
    converter.wrap_links = False
    return converter.handle(html)


def get_page(session: requests.Session, url: str) -> tuple[str, BeautifulSoup] | None:
    """Fetch a URL and return (raw_html, soup). Returns None on failure."""
    try:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        return resp.text, soup
    except requests.RequestException as e:
        print(f"  [skip] {url} — {e}")
        return None


def collect_links(soup: BeautifulSoup, base_url: str, base_domain: str) -> list[str]:
    """
    Extract all internal doc links from a page.
    Only keeps links that share the same base domain and path prefix.
    """
    base_path = "/".join(urlparse(base_url).path.split("/")[:-1])
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#")[0].strip()
        if not href:
            continue
        full = urljoin(base_url, href)
        parsed = urlparse(full)
        if (
            parsed.scheme in ("http", "https")
            and parsed.hostname == base_domain
            and parsed.path.startswith(base_path)
            and parsed.path != urlparse(base_url).path
        ):
            links.append(full)
    return list(dict.fromkeys(links))   # deduplicated, order-preserved


def collect_links_from_sitemap(
    session: requests.Session,
    base_url: str,
    base_domain: str,
) -> list[str]:
    """Collect links from sitemap.xml if available.

    This is useful for docs sites that render nav links client-side,
    where static HTML contains only a small subset of pages.
    """
    parsed_base = urlparse(base_url)
    base_parts = [p for p in parsed_base.path.split("/") if p]
    # Keep crawls focused by section, e.g. /docs/v5 when started from /docs/v5/intro.
    if len(base_parts) >= 2:
        path_prefix = "/" + "/".join(base_parts[:2])
    elif base_parts:
        path_prefix = "/" + base_parts[0]
    else:
        path_prefix = "/docs"
    # Try docs-local sitemap first, then host-level sitemap.
    sitemap_candidates = [
        urljoin(base_url, "sitemap.xml"),
        f"{parsed_base.scheme}://{base_domain}/docs/sitemap.xml",
        f"{parsed_base.scheme}://{base_domain}/sitemap.xml",
    ]

    links: list[str] = []
    for sitemap_url in sitemap_candidates:
        try:
            resp = session.get(sitemap_url, timeout=15)
            resp.raise_for_status()
        except requests.RequestException:
            continue

        loc_matches = re.findall(r"<loc>(.*?)</loc>", resp.text, flags=re.IGNORECASE | re.DOTALL)
        for raw_loc in loc_matches:
            url = (raw_loc or "").strip()
            if not url:
                continue

            p = urlparse(url)
            if p.scheme not in ("http", "https"):
                continue
            if p.hostname != base_domain:
                continue
            if not p.path.startswith(path_prefix):
                continue

            # Skip utility pages that are not useful as API reference docs.
            if p.path in ("/docs/search", "/docs/markdown-page"):
                continue

            links.append(url)

        # First successful sitemap is enough.
        if links:
            break

    return list(dict.fromkeys(links))


def page_description(soup: BeautifulSoup) -> str:
    """Extract a one-line description from meta or first paragraph."""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        return meta["content"].strip()[:120]
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if len(text) > 30:
            return text[:120].rstrip() + ("…" if len(text) > 120 else "")
    return ""


# ── main ───────────────────────────────────────────────────────────────────────

def crawl(index_url: str, max_pages: int) -> None:
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (docs-crawler; educational use)"

    print(f"Fetching index: {index_url}")
    result = get_page(session, index_url)
    if result is None:
        sys.exit("Failed to fetch the index page.")

    _, index_soup = result
    framework = framework_name_from(index_url, index_soup)
    base_domain = urlparse(index_url).hostname

    out_dir = Path("docs") / framework
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output dir   : {out_dir}/")
    print(f"Framework    : {framework}")

    # Build queue from sitemap when available; fallback to page links.
    sitemap_links = collect_links_from_sitemap(session, index_url, base_domain)
    if sitemap_links:
        print(f"Sitemap links: {len(sitemap_links)}")
        to_visit = [index_url] + sitemap_links
    else:
        to_visit = [index_url] + collect_links(index_soup, index_url, base_domain)
    to_visit = list(dict.fromkeys(to_visit))[:max_pages]

    existing_names: set[str] = set()
    index_entries: list[dict] = []   # {filename, url, title, description}

    for i, url in enumerate(to_visit, 1):
        print(f"[{i:>3}/{len(to_visit)}] {url}")
        result = get_page(session, url)
        if result is None:
            continue

        raw_html, soup = result

        # Extract main content only (avoids nav/footer noise)
        main = (
            soup.find("main")
            or soup.find("article")
            or soup.find(id=re.compile(r"content|main|body", re.I))
            or soup.find("body")
            or soup
        )

        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True).split("|")[0].split("—")[0].strip() if title_tag else url
        description = page_description(soup)
        filename = page_filename(url, title, existing_names)
        markdown = html_to_markdown(str(main), url)

        # Prepend a header with metadata so I can orient quickly
        header = (
            f"# {title}\n\n"
            f"> **Source:** {url}\n\n"
            "---\n\n"
        )
        (out_dir / filename).write_text(header + markdown, encoding="utf-8")

        index_entries.append({"filename": filename, "url": url, "title": title, "description": description})
        time.sleep(0.3)   # be polite to the server

    # ── write master index ────────────────────────────────────────────────────
    lines = [
        f"# {framework} — Documentation Index\n",
        f"Crawled from: {index_url}\n",
        f"Pages saved : {len(index_entries)}\n",
        f"Generated   : {time.strftime('%Y-%m-%d %H:%M')}\n",
        "\n---\n",
        "| File | Title | Description |\n",
        "|------|-------|-------------|\n",
    ]
    for e in index_entries:
        desc = e["description"].replace("|", "\\|")
        lines.append(f"| [{e['filename']}]({e['filename']}) | {e['title']} | {desc} |\n")

    (out_dir / "_index.md").write_text("".join(lines), encoding="utf-8")
    print(f"\nDone. {len(index_entries)} pages saved to {out_dir}/")
    print(f"Master index  : {out_dir}/_index.md")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", help="URL of the documentation index page")
    parser.add_argument("--max-pages", type=int, default=200, metavar="N",
                        help="Maximum number of pages to crawl (default: 200)")
    args = parser.parse_args()
    crawl(args.url, args.max_pages)


if __name__ == "__main__":
    main()
