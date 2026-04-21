Input:  same results_dir as Phase 1/2
        one signature (selected from Phase 2 verdict table)
        
Sections:

1. Signature Card
   ─────────────
   alias + full sig string
   summary table: one row per (coin, TF) with all Phase 1 metrics
   from the per-symbol CSVs
   colour coded pass/fail per cell

2. Equity Curves
   ─────────────
   cumulative return curve per (coin, TF) from trade log
   window bands overlaid (Bear / Recovery / Bull shaded)
   all coins on one chart (toggle to split by TF)
   portfolio aggregate line (equal-weighted across coins)

3. Drawdown Series
   ────────────────
   rolling max-drawdown per (coin, TF)
   highlights period and depth of worst drawdown
   Bear window shaded — did DD cluster there or spread?

4. Monthly PnL Heatmap
   ────────────────────
   rows = coins (or coin_TF conditions)
   cols = calendar months
   cell = sum of Return [%] for that month
   immediately shows whether losses cluster in specific months/regime

5. Regime Filter Diagnostic
   ─────────────────────────
   trade count per month bar chart (all coins aggregated)
   Bear/Recovery/Bull shaded
   KEY QUESTION: does trade count drop significantly in Bear?
   if not → regime filter isn't gating, which is why Bear bleeds

6. Trade Distribution
   ───────────────────
   histogram of Return [%] per trade
   split by window (Bear / Recovery / Bull)
   shows if Bear losses come from fat left tails or just many small losers
   win/loss streak table

7. Best/Worst Trade Log
   ─────────────────────
   top 10 wins and top 10 losses with EntryTime, ExitTime, coin, TF
   lets you spot if one or two large trades are distorting metrics