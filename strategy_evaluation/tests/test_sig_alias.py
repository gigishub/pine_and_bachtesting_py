"""Tests for strategy_evaluation.sig_alias."""

from __future__ import annotations

import pytest

from strategy_evaluation.sig_alias import sig_to_alias


# ── 5-param examples from the user spec ──────────────────────────────────────

def test_all_on_except_last() -> None:
    sig = "use_adx=1|use_ema_ribbon=1|use_chandelier=1|use_psar=1|use_trailing_stop=0"
    assert sig_to_alias(sig) == "ABCD_11110"


def test_middle_two_on() -> None:
    sig = "use_adx=0|use_ema_ribbon=1|use_chandelier=1|use_psar=0|use_trailing_stop=0"
    assert sig_to_alias(sig) == "BC_01100"


def test_all_five_on() -> None:
    sig = "use_adx=1|use_ema_ribbon=1|use_chandelier=1|use_psar=1|use_trailing_stop=1"
    assert sig_to_alias(sig) == "ABCDE_11111"


def test_last_four_on() -> None:
    sig = "use_adx=0|use_ema_ribbon=1|use_chandelier=1|use_psar=1|use_trailing_stop=1"
    assert sig_to_alias(sig) == "BCDE_01111"


def test_first_only_on() -> None:
    sig = "use_adx=1|use_ema_ribbon=0|use_chandelier=0|use_psar=0|use_trailing_stop=0"
    assert sig_to_alias(sig) == "A_10000"


def test_all_five_off() -> None:
    sig = "use_adx=0|use_ema_ribbon=0|use_chandelier=0|use_psar=0|use_trailing_stop=0"
    assert sig_to_alias(sig) == "NONE_00000"


# ── 3-param (fewer than 5) ────────────────────────────────────────────────────

def test_three_params_mixed() -> None:
    sig = "use_adx=1|use_ema_ribbon=0|use_chandelier=1"
    assert sig_to_alias(sig) == "AC_101"


def test_three_params_all_on() -> None:
    sig = "use_adx=1|use_ema_ribbon=1|use_chandelier=1"
    assert sig_to_alias(sig) == "ABC_111"


def test_three_params_all_off() -> None:
    sig = "use_adx=0|use_ema_ribbon=0|use_chandelier=0"
    assert sig_to_alias(sig) == "NONE_000"


# ── 10-param (more than 5) ────────────────────────────────────────────────────

def test_ten_params_all_on() -> None:
    parts = [f"use_f{i}=1" for i in range(10)]
    sig = "|".join(parts)
    assert sig_to_alias(sig) == "ABCDEFGHIJ_1111111111"


def test_ten_params_alternating() -> None:
    parts = [f"use_f{i}={'1' if i % 2 == 0 else '0'}" for i in range(10)]
    sig = "|".join(parts)
    assert sig_to_alias(sig) == "ACEGI_1010101010"


# ── True/False values (VBT boolean columns) ──────────────────────────────────

def test_true_false_values() -> None:
    sig = "use_adx=True|use_ema_ribbon=False|use_chandelier=True"
    assert sig_to_alias(sig) == "AC_101"


def test_mixed_01_and_true_false() -> None:
    sig = "use_adx=1|use_ema_ribbon=False|use_chandelier=True|use_psar=0"
    assert sig_to_alias(sig) == "AC_1010"


def test_case_insensitive_true_false() -> None:
    sig = "use_adx=TRUE|use_ema_ribbon=FALSE|use_chandelier=true"
    assert sig_to_alias(sig) == "AC_101"


# ── Escaped pipe separator ────────────────────────────────────────────────────

def test_escaped_pipe() -> None:
    sig = r"use_adx=1\|use_ema_ribbon=0\|use_chandelier=1"
    assert sig_to_alias(sig) == "AC_101"


# ── Edge / fallback cases ─────────────────────────────────────────────────────

def test_single_param_on() -> None:
    assert sig_to_alias("use_adx=1") == "A_1"


def test_single_param_off() -> None:
    assert sig_to_alias("use_adx=0") == "NONE_0"


def test_malformed_no_equals_returns_sig() -> None:
    """No parseable bits → return original string as fallback."""
    bad = "this_is_not_a_signature"
    assert sig_to_alias(bad) == bad


def test_empty_string_returns_empty() -> None:
    assert sig_to_alias("") == ""


def test_extra_whitespace_around_values() -> None:
    sig = "use_adx= 1 |use_ema_ribbon= 0 |use_chandelier= 1 "
    assert sig_to_alias(sig) == "AC_101"
