"""Entrypoint for the multi-dataset filter-finding workflow.

The heavy lifting lives under the robustness package so this entrypoint stays
small and readable while still running the full six-step search process.
"""

from __future__ import annotations

from .robustness import (
    DEFAULT_MATRIX_CONFIG,
    build_baseline_params,
    print_consistency_report,
    print_dataset_summary,
    print_intersection_report,
    print_master_winners_report,
    print_matrix_plan,
    print_out_of_sample_report,
    run_filter_matrix_search,
)


if __name__ == "__main__":
    baseline_params = build_baseline_params()
    print_matrix_plan(DEFAULT_MATRIX_CONFIG)

    artifacts = run_filter_matrix_search(
        baseline_params,
        DEFAULT_MATRIX_CONFIG,
    )

    print_dataset_summary(artifacts, DEFAULT_MATRIX_CONFIG.top_n)
    print_master_winners_report(artifacts)
    print_intersection_report(artifacts)
    print_consistency_report(artifacts)
    print_out_of_sample_report(artifacts)
