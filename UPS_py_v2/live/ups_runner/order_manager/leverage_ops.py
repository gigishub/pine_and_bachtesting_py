from __future__ import annotations

from typing import TYPE_CHECKING

from .error_policy import bybit_ret_code

if TYPE_CHECKING:
    from ...bybit_client import BybitV5Client
    from ..common.live_logger import LiveLogger
    from ..config import LiveConfig


class LeverageOps:
    """Leverage-related helpers and policies."""

    # Provided by OrderManager facade. Declared here for static type checkers.
    if TYPE_CHECKING:
        client: BybitV5Client
        cfg: LiveConfig
        logger: LiveLogger

    def _set_leverage_with_fallback(self, target_leverage: float, *, reason: str) -> bool:
        """Try to set leverage and optionally soft-fail on known exchange constraints."""
        try:
            self.client.set_leverage(
                category=self.cfg.category,
                symbol=self.cfg.symbol,
                leverage=target_leverage,
            )
            self.logger.log(f"Leverage set to {target_leverage}x for {self.cfg.symbol} ({reason})")
            return True
        except RuntimeError as exc:
            msg = str(exc).lower()
            code = bybit_ret_code(exc)
            if "not modified" in msg:
                self.logger.log(f"Leverage already {target_leverage}x on exchange; continuing.")
                return True

            # 110012: not enough available balance to apply requested leverage.
            if self.cfg.leverage_fail_soft and code == "110012":
                self.logger.log(
                    "Leverage update rejected by Bybit (110012: insufficient balance for new leverage). "
                    "Continuing with current exchange leverage."
                )
                return False

            if self.cfg.leverage_fail_soft:
                self.logger.log(f"Leverage update failed; continuing due to leverage_fail_soft=True. Details: {exc}")
                return False
            raise

    def maybe_apply_auto_leverage(self, entry: float, stop: float) -> None:
        """Optionally set leverage from stop distance, capped by configured bounds.

        Heuristic: leverage ~= 1 / (stop_distance_pct + buffer_pct).
        This is an approximation and does not model full liquidation mechanics.
        """
        if self.cfg.dry_run:
            return
        if self.cfg.category not in {"linear", "inverse"}:
            return
        if not self.cfg.auto_leverage_by_stop:
            return
        if entry <= 0:
            return

        stop_distance_pct = abs(entry - stop) / entry
        safety_buffer_pct = max(0.0, self.cfg.auto_leverage_sl_buffer_pct) / 100.0
        min_liq_gap_pct = stop_distance_pct + safety_buffer_pct
        if min_liq_gap_pct <= 0:
            return

        target = 1.0 / min_liq_gap_pct
        target = max(self.cfg.auto_leverage_min, min(self.cfg.auto_leverage_max, target))
        target = round(target, 2)
        self._set_leverage_with_fallback(target, reason="auto-by-stop")

    def apply_leverage_if_configured(self) -> None:
        """Set symbol leverage for derivatives categories when configured."""
        if self.cfg.dry_run:
            return
        if self.cfg.category not in {"linear", "inverse"}:
            return

        target_leverage = 1.0 if self.cfg.force_no_leverage else self.cfg.leverage
        if target_leverage <= 0:
            return

        reason = "force-no-leverage" if self.cfg.force_no_leverage else "fixed"
        self._set_leverage_with_fallback(target_leverage, reason=reason)
