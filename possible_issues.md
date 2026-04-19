1. The Rank bug (crash) — already discussed. Sections 3 and 4 always crash when any toggle is forced. The fix is the _sort_best_first helper in consistency.py.\



2. Force ON a toggle that is always False in the data (e.g. use_power_candle):

_analysis_raw = _analysis_raw[_analysis_raw["use_power_candle"] == 1]
# → 0 rows, because it was never True in any CSV


This produces an empty DataFrame → ML returns None → Sections 5 & 6 show "Not enough data", Section 3/4 will show empty. The st.stop() guards are missing for this case.

Summary
The architecture is correct — TF and toggle filters propagate properly to all sections and cache invalidation works. The only broken things are:

KeyError: 'Rank' crashes sections 3 & 4 on any toggle force
No guard for Force ON a toggle that never exists → empty df silent failure
Sections 5 & 6 not reacting to threshold sliders is correct behavior, not a bug.