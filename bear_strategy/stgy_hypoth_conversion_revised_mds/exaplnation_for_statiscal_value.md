Sure. Let's build it from scratch with one simple idea.

---

**The one idea you need:**

Every result you measure has two parts:
```
what you measured  =  real effect  +  random luck
```

You can't remove luck. But you can measure how much luck is *possible* given your sample size. If your result is much bigger than the maximum likely luck, it's real.

---

**Step 1 — measure the possible luck**

```
# p    = your baseline win rate (e.g. 0.3966)
# n    = number of trades in the smaller group
# noise = how much your result could move from pure luck alone

noise = sqrt( p * (1 - p) / n )
```

Think of noise as: *"if this filter did absolutely nothing, results would still randomly drift by this much."*

More trades → smaller noise → easier to see real effects.

---

**Step 2 — measure your signal**

```
# how much did the filter actually move the win rate?

signal = filtered_win_rate - baseline_win_rate
```

---

**Step 3 — is the signal bigger than the luck?**

```
# 2.5 means: "I want to be 99% sure this isn't luck"
# if signal is more than 2.5x the possible luck, it's real

if signal > 2.5 * noise:
    REAL   → trust this filter, move to next step
else:
    NOISE  → do not trust, get more data or cut the filter
```

---

**Complete pseudocode to save:**

```python
def is_filter_real(baseline_wr, filtered_wr, n):

    # how much could luck alone move the result?
    noise = sqrt( baseline_wr * (1 - baseline_wr) / n )

    # how much did the filter actually move it?
    signal = filtered_wr - baseline_wr

    # is the signal 2.5x bigger than the luck?
    z = signal / noise

    if z > 2.5:
        return "REAL — filter is trustworthy"
    else:
        return "NOISE — do not trust this result"

# run it like this:
is_filter_real(
    baseline_wr = 0.3966,   # all-candle win rate
    filtered_wr = 0.4273,   # filtered population win rate
    n           = 94176     # trades in the smaller group
)

# result: z = 19.3 → REAL
```

---

**What each number in your actual data means in one line each:**

```
noise  = 0.0016   # luck could randomly move results by 0.16pp
signal = 0.0307   # your filter actually moved results by 3.07pp
z      = 19.3     # your signal is 19x bigger than luck
                  # anything above 2.5 is trustworthy
                  # 19x means this is not luck. at all.
```

---

The only number you need to remember is **2.5**. If your signal divided by your noise is above 2.5, the result is real. Below 2.5, get more data before trusting it.