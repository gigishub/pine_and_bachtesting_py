"""Tests for strategy_evaluation.consistency."""

from __future__ import annotations

import pandas as pd
import pytest

from strategy_evaluation.config import RobustnessConfig
from strategy_evaluation.consistency import symbol_pass_rate, timeframe_pass_rate, toggle_frequency, sweep_threshold, compute_toggle_consensus


@pytest.fixture()
def cfg() -> RobustnessConfig:
    return RobustnessConfig()


def _make_df(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def _passing_combo(symbol: str, tf: str, rank: int = 1, **overrides: object) -> dict:
    base = {
        "Symbol": symbol,
        "Timeframe": tf,
        "Parameter Signature": f"use_adx=1",
        "Rank": rank,
        "SQN": 1.5,
        "Profit Factor": 2.0,
        "# Trades": 30,
        "Win Rate [%]": 40.0,
        "Sharpe Ratio": 0.8,
        "Return [%]": 25.0,
        "use_adx": 1,
        "use_ema": 0,
    }
    base.update(overrides)
    return base


def _failing_combo(symbol: str, tf: str, rank: int = 2) -> dict:
    return _passing_combo(symbol, tf, rank=rank, SQN=0.1, **{"Profit Factor": 1.0})


class TestSymbolPassRate:
    def test_symbol_with_passing_combo(self, cfg: RobustnessConfig) -> None:
        df = _make_df([_passing_combo("BTCUSDT", "4H"), _failing_combo("ETHUSDT", "4H")])
        rates = symbol_pass_rate(df, cfg)
        assert rates["BTCUSDT"] == 1.0
        assert rates["ETHUSDT"] == 0.0

    def test_all_symbols_fail(self, cfg: RobustnessConfig) -> None:
        df = _make_df([_failing_combo("BTCUSDT", "4H"), _failing_combo("ETHUSDT", "4H")])
        rates = symbol_pass_rate(df, cfg)
        assert all(v == 0.0 for v in rates.values())

    def test_symbol_passes_on_any_timeframe(self, cfg: RobustnessConfig) -> None:
        df = _make_df([
            _failing_combo("BTCUSDT", "1H"),
            _passing_combo("BTCUSDT", "4H"),
        ])
        rates = symbol_pass_rate(df, cfg)
        assert rates["BTCUSDT"] == 1.0


class TestTimeframePassRate:
    def test_rate_is_fraction_of_symbols(self, cfg: RobustnessConfig) -> None:
        df = _make_df([
            _passing_combo("BTCUSDT", "4H"),
            _failing_combo("ETHUSDT", "4H"),
        ])
        rates = timeframe_pass_rate(df, cfg)
        assert rates["4H"] == pytest.approx(0.5)

    def test_full_pass_rate(self, cfg: RobustnessConfig) -> None:
        df = _make_df([
            _passing_combo("BTCUSDT", "1H"),
            _passing_combo("ETHUSDT", "1H"),
        ])
        rates = timeframe_pass_rate(df, cfg)
        assert rates["1H"] == pytest.approx(1.0)


class TestToggleFrequency:
    def test_counts_enabled_toggles(self, cfg: RobustnessConfig) -> None:
        df = _make_df([
            _passing_combo("BTCUSDT", "4H", use_adx=1, use_ema=0),
            _passing_combo("ETHUSDT", "4H", use_adx=1, use_ema=1),
        ])
        freq = toggle_frequency(df, cfg)
        assert freq.get("use_adx", 0) == 2
        assert freq.get("use_ema", 0) == 1

    def test_empty_result_for_no_toggles(self, cfg: RobustnessConfig) -> None:
        # DataFrame with no boolean-style columns beyond metadata
        df = _make_df([_passing_combo("BTCUSDT", "4H")])
        freq = toggle_frequency(df, cfg)
        assert isinstance(freq, dict)


class TestMinComboPassRate:
    def test_strict_threshold_requires_all_combos_pass(self) -> None:
        """min_combo_pass_rate=1.0 means every combo must pass — one failing combo fails the symbol."""
        cfg = RobustnessConfig(min_combo_pass_rate=1.0)
        df = _make_df([
            _passing_combo("BTCUSDT", "4H", rank=1),
            _failing_combo("BTCUSDT", "4H", rank=2),  # 50% pass rate < 100%
        ])
        rates = symbol_pass_rate(df, cfg)
        assert rates["BTCUSDT"] == 0.0

    def test_strict_threshold_passes_when_all_pass(self) -> None:
        """min_combo_pass_rate=1.0 still passes a symbol when every combo passes."""
        cfg = RobustnessConfig(min_combo_pass_rate=1.0)
        df = _make_df([
            _passing_combo("BTCUSDT", "4H", rank=1),
            _passing_combo("BTCUSDT", "4H", rank=2),
        ])
        rates = symbol_pass_rate(df, cfg)
        assert rates["BTCUSDT"] == 1.0

    def test_zero_threshold_matches_any_logic(self) -> None:
        """min_combo_pass_rate=0.0 — any single passing combo makes the symbol pass (old behaviour)."""
        cfg = RobustnessConfig(min_combo_pass_rate=0.0)
        df = _make_df([
            _passing_combo("BTCUSDT", "4H", rank=1),
            _failing_combo("BTCUSDT", "4H", rank=2),
            _failing_combo("BTCUSDT", "4H", rank=3),
        ])
        # mean=1/3≈0.33 ≥ 0.0 → passes
        rates = symbol_pass_rate(df, cfg)
        assert rates["BTCUSDT"] == 1.0

    def test_partial_threshold(self) -> None:
        """Intermediate min_combo_pass_rate correctly gates on fraction."""
        cfg = RobustnessConfig(min_combo_pass_rate=0.50)
        # 1 of 3 pass → 33% < 50% → fails
        df_fail = _make_df([
            _passing_combo("BTCUSDT", "4H", rank=1),
            _failing_combo("BTCUSDT", "4H", rank=2),
            _failing_combo("BTCUSDT", "4H", rank=3),
        ])
        assert symbol_pass_rate(df_fail, cfg)["BTCUSDT"] == 0.0

        # 2 of 3 pass → 67% ≥ 50% → passes
        df_pass = _make_df([
            _passing_combo("BTCUSDT", "4H", rank=1),
            _passing_combo("BTCUSDT", "4H", rank=2),
            _failing_combo("BTCUSDT", "4H", rank=3),
        ])
        assert symbol_pass_rate(df_pass, cfg)["BTCUSDT"] == 1.0


class TestSweepThreshold:
    def _multi_combo_df(self) -> pd.DataFrame:
        """DataFrame with one symbol/TF, combos spanning SQN 0.5 to 2.0."""
        rows = [
            _passing_combo("BTCUSDT", "4H", rank=i, SQN=sqn)
            for i, sqn in enumerate([0.5, 1.0, 1.5, 2.0], start=1)
        ]
        return _make_df(rows)

    def test_output_has_one_row_per_sweep_value(self) -> None:
        cfg = RobustnessConfig()
        df = self._multi_combo_df()
        sweep_vals = [0.5, 1.0, 1.5, 2.0]
        result = sweep_threshold(df, "SQN", sweep_vals, cfg)
        assert len(result) == len(sweep_vals)
        assert list(result.columns) == ["threshold", "symbol_pass_rate", "tf_pass_rate"]

    def test_symbol_pass_rate_non_increasing_as_threshold_tightens(self) -> None:
        """As the SQN threshold rises, pass rate should not increase."""
        cfg = RobustnessConfig(min_combo_pass_rate=0.0)  # lenient combo gate
        df = self._multi_combo_df()
        sweep_vals = [0.5, 1.0, 1.5, 2.0, 2.5]
        result = sweep_threshold(df, "SQN", sweep_vals, cfg)
        rates = result["symbol_pass_rate"].tolist()
        # Each step should be ≤ the previous step
        for prev, curr in zip(rates, rates[1:]):
            assert curr <= prev + 1e-9, f"Pass rate increased: {prev} → {curr}"

    def test_invalid_metric_col_raises(self) -> None:
        cfg = RobustnessConfig()
        df = self._multi_combo_df()
        with pytest.raises(ValueError, match="metric_col"):
            sweep_threshold(df, "UnknownColumn", [1.0, 2.0], cfg)

    def test_does_not_mutate_cfg(self) -> None:
        """sweep_threshold must not modify the passed cfg object."""
        cfg = RobustnessConfig(min_sqn=1.0)
        df = self._multi_combo_df()
        sweep_threshold(df, "SQN", [0.5, 1.5, 2.5], cfg)
        assert cfg.min_sqn == 1.0


class TestToggleConsensus:
    """Tests for compute_toggle_consensus()."""

    def _annotated_df(self, toggle_a: int, toggle_b: int, sqn: float, passes: bool) -> pd.DataFrame:
        """Build a single-row annotated DataFrame for consensus testing."""
        return pd.DataFrame([{
            "Symbol": "BTCUSDT",
            "Timeframe": "4H",
            "Parameter Signature": "sig",
            "Rank": 1,
            "SQN": sqn,
            "Profit Factor": 2.0,
            "# Trades": 30,
            "Win Rate [%]": 50.0,
            "Sharpe Ratio": 1.0,
            "Return [%]": 30.0,
            "toggle_a": toggle_a,
            "toggle_b": toggle_b,
            "_passes": passes,
        }])

    def _make_ols(self, toggle: str, coeff: float, p_value: float, sig: bool) -> object:
        """Return a minimal OLSResult-like mock."""
        from strategy_evaluation.significance import OLSResult
        table = pd.DataFrame([{
            "toggle": toggle, "coefficient": coeff, "std_err": 0.01,
            "t_stat": coeff / 0.01, "p_value": p_value, "significant": sig,
        }])
        return OLSResult(table=table, target_col="SQN", n_combos=10, r_squared=0.5)

    def _make_shap(self, toggle: str, mean_val: float) -> object:
        """Return a minimal ShapResult-like mock."""
        from strategy_evaluation.importance import ShapResult
        mean_shap = pd.Series({toggle: mean_val})
        return ShapResult(
            mean_shap=mean_shap,
            abs_mean_shap=mean_shap.abs().sort_values(ascending=False),
            target_col="SQN",
            n_combos=10,
            toggle_cols=[toggle],
        )

    def test_unanimous_keep(self) -> None:
        """All three signals agree toggle_a is beneficial → consensus = Keep ON."""
        cfg = RobustnessConfig()
        # Build 5 passing combos across 5 symbols with toggle_a=1 always
        rows = []
        for i in range(5):
            rows.append({
                "Symbol": f"SYM{i}", "Timeframe": "4H",
                "Parameter Signature": "sig", "Rank": 1,
                "SQN": 2.0, "Profit Factor": 2.0, "# Trades": 30,
                "Win Rate [%]": 50.0, "Sharpe Ratio": 1.0, "Return [%]": 30.0,
                "toggle_a": 1, "_passes": True,
            })
        df = pd.DataFrame(rows)
        ols = self._make_ols("toggle_a", coeff=0.5, p_value=0.01, sig=True)
        shap = self._make_shap("toggle_a", mean_val=0.1)

        result = compute_toggle_consensus(df, cfg, ols, shap)

        row = result[result["toggle"] == "toggle_a"]
        assert not row.empty, "toggle_a not found in consensus output"
        assert row.iloc[0]["consensus"] == "✅ Keep ON"

    def test_keep_on_with_small_positive_shap(self) -> None:
        """SHAP=+0.010 (below old 0.02 noise floor) should still yield Keep ON.

        All three signals agree the toggle helps. The old code required SHAP > noise_floor
        which blocked this case. The fix uses direction only (SHAP > 0) for Keep ON.
        """
        cfg = RobustnessConfig()
        rows = []
        for i in range(5):
            rows.append({
                "Symbol": f"SYM{i}", "Timeframe": "4H",
                "Parameter Signature": "sig", "Rank": 1,
                "SQN": 2.0, "Profit Factor": 2.0, "# Trades": 30,
                "Win Rate [%]": 50.0, "Sharpe Ratio": 1.0, "Return [%]": 30.0,
                "toggle_a": 1, "_passes": True,
            })
        df = pd.DataFrame(rows)
        ols = self._make_ols("toggle_a", coeff=0.32, p_value=0.03, sig=True)
        shap = self._make_shap("toggle_a", mean_val=0.010)  # below old 0.02 noise floor

        result = compute_toggle_consensus(df, cfg, ols, shap)

        row = result[result["toggle"] == "toggle_a"]
        assert not row.empty, "toggle_a not found in consensus output"
        assert row.iloc[0]["consensus"] == "✅ Keep ON", (
            f"Expected ✅ Keep ON but got: {row.iloc[0]['consensus']}. "
            "Small positive SHAP should use direction-only check."
        )

    def test_unanimous_remove(self) -> None:
        """All three signals agree toggle_b is harmful → consensus = Remove."""
        cfg = RobustnessConfig()
        # Build 5 passing combos across 5 symbols with toggle_b=0 always, toggle_a=1
        rows = []
        for i in range(5):
            rows.append({
                "Symbol": f"SYM{i}", "Timeframe": "4H",
                "Parameter Signature": "sig", "Rank": 1,
                "SQN": 1.5, "Profit Factor": 2.0, "# Trades": 30,
                "Win Rate [%]": 50.0, "Sharpe Ratio": 1.0, "Return [%]": 20.0,
                "toggle_a": 1, "toggle_b": 0, "_passes": True,
            })
        df = pd.DataFrame(rows)
        ols = self._make_ols("toggle_b", coeff=-0.5, p_value=0.01, sig=True)
        shap = self._make_shap("toggle_b", mean_val=-0.1)

        result = compute_toggle_consensus(df, cfg, ols, shap)

        row = result[result["toggle"] == "toggle_b"]
        assert not row.empty, "toggle_b not found in consensus output"
        assert row.iloc[0]["consensus"] == "❌ Remove"

    def test_empty_when_no_passing_combos(self) -> None:
        """Returns an empty DataFrame (correct columns) when no combos pass."""
        cfg = RobustnessConfig()
        df = pd.DataFrame([{
            "Symbol": "BTCUSDT", "Timeframe": "4H",
            "Parameter Signature": "sig", "Rank": 1,
            "SQN": 0.1, "Profit Factor": 0.5, "# Trades": 5,
            "Win Rate [%]": 20.0, "Sharpe Ratio": 0.1, "Return [%]": 1.0,
            "toggle_a": 1, "_passes": False,
        }])
        result = compute_toggle_consensus(df, cfg, None, None)
        assert result.empty
        assert list(result.columns) == [
            "toggle", "freq_pct", "ols_coeff", "ols_p", "ols_sig", "shap_mean", "consensus"
        ]
