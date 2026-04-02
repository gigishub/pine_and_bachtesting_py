from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .error_policy import bybit_ret_code, is_non_fatal_stop_error, is_unchanged_stop_error
from .tpsl_policy import build_trading_stop_plan

if TYPE_CHECKING:
    from ...bybit_client import BybitV5Client, InstrumentSpec
    from ..common.live_logger import LiveLogger
    from ..config import LiveConfig


class StopOps:
    """Generic TP/SL lifecycle and fallback handling."""

    # Provided by OrderManager facade. Declared here for static type checkers.
    if TYPE_CHECKING:
        client: BybitV5Client
        cfg: LiveConfig
        instrument: InstrumentSpec
        logger: LiveLogger
        # Implemented by TrailStopOps in the composed OrderManager.
        def prepare_trailing_mode(self, *, position_side: str, clear_take_profit: bool) -> None: ...

    def _attempt_single_side_update(
        self,
        payload: dict[str, Any],
        *,
        start_log: str,
        success_log: str,
        unchanged_log: str,
        nonfatal_log_prefix: str,
        retry_after_success: bool,
        retry_after_unchanged: bool,
    ) -> str:
        self.logger.log(start_log)
        try:
            self.client.set_trading_stop(payload)
            self.logger.log(success_log)
            return "retry" if retry_after_success else "success"
        except RuntimeError as exc:
            code = bybit_ret_code(exc)
            if code == "34040":
                self.logger.log(unchanged_log)
                return "retry" if retry_after_unchanged else "success"
            if code in {"10001", "110007"}:
                self.logger.log(f"{nonfatal_log_prefix} (non-fatal, retCode {code}); continuing.")
                return "next"
            raise

    def _attempt_emergency_updates(
        self,
        *,
        sl_only_payload: dict[str, Any] | None,
        tp_only_payload: dict[str, Any] | None,
        prefix: str,
    ) -> bool:
        if sl_only_payload is not None:
            status = self._attempt_single_side_update(
                sl_only_payload,
                start_log=f"{prefix}attempting emergency SL-only update.",
                success_log="Emergency SL-only update succeeded.",
                unchanged_log="SL unchanged on exchange (retCode 34040); continuing.",
                nonfatal_log_prefix="Emergency SL-only update rejected",
                retry_after_success=False,
                retry_after_unchanged=False,
            )
            if status == "success":
                return True
            if tp_only_payload is None:
                return False

        if tp_only_payload is None:
            return False

        sl_still_missing = sl_only_payload is not None
        status = self._attempt_single_side_update(
            tp_only_payload,
            start_log=f"{prefix}attempting emergency TP-only update.",
            success_log=(
                "WARNING: Emergency TP-only update succeeded but SL was not set; queuing retry to set SL."
                if sl_still_missing
                else "Emergency TP-only update succeeded."
            ),
            unchanged_log=(
                "TP already set (retCode 34040) but SL not set; queuing retry to set SL."
                if sl_still_missing
                else "TP unchanged on exchange (retCode 34040); continuing."
            ),
            nonfatal_log_prefix="Emergency TP-only update rejected",
            retry_after_success=sl_still_missing,
            retry_after_unchanged=sl_still_missing,
        )
        return status == "success"

    def update_stops(
        self,
        stop_loss: float | None,
        take_profit: float | None,
        *,
        position_size: float,
        position_side: str,
    ) -> bool:
        """Set stop-loss and/or take-profit on the exchange. No-op for spot."""
        if self.cfg.category not in {"linear", "inverse"}:
            return True

        plan = build_trading_stop_plan(
            self.cfg,
            self.instrument,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position_size,
            position_side=position_side,
        )

        if self.cfg.dry_run:
            self.logger.log(f"DRY-RUN TP/SL {plan.payload}")
            return True

        self.prepare_trailing_mode(position_side=position_side, clear_take_profit=plan.clear_take_profit)

        try:
            self.client.set_trading_stop(plan.payload)
            return True
        except RuntimeError as exc:
            # Bybit returns retCode 34040 when submitted TP/SL is unchanged.
            # This is not an execution failure and should not stop the runner loop.
            code = bybit_ret_code(exc)
            if is_unchanged_stop_error(exc):
                self.logger.log("TP/SL unchanged on exchange (retCode 34040); continuing.")
                return True

            # TP/SL may become invalid momentarily as mark price moves.
            # For partial TP/SL, invalid parameter (10001) may happen due API checks.
            # Retry once in Full TP/SL mode to ensure we still have protective exits.
            if code == "10001" and plan.use_partial_tp_limit:
                self.logger.log(
                    "TP/SL update rejected with 10001 in partial mode; retrying with Full mode fallback."
                )
                try:
                    self.client.set_trading_stop(plan.full_payload)
                    self.logger.log("TP/SL update succeeded after Full mode fallback.")
                    return True
                except RuntimeError as exc2:
                    code2 = bybit_ret_code(exc2)
                    if code2 == "34040":
                        self.logger.log("TP/SL unchanged on exchange (retCode 34040); continuing.")
                        return True
                    if code2 == "10001":
                        return self._attempt_emergency_updates(
                            sl_only_payload=plan.sl_only_payload,
                            tp_only_payload=plan.tp_only_payload,
                            prefix="Fallback TP/SL still invalid; ",
                        )
                    if is_non_fatal_stop_error(exc2):
                        self.logger.log(
                            f"TP/SL update rejected on fallback (non-fatal, retCode {code2}); continuing."
                        )
                        return False
                    raise

            if code == "10001":
                return self._attempt_emergency_updates(
                    sl_only_payload=plan.sl_only_payload,
                    tp_only_payload=plan.tp_only_payload,
                    prefix="TP/SL update invalid; ",
                )

            if is_non_fatal_stop_error(exc):
                self.logger.log(f"TP/SL update rejected by exchange (non-fatal, retCode {code}); continuing.")
                return False
            raise
