"""Truth Table 單元測試（CURSOR_IMPLEMENTATION_GUIDE Section 3）。"""

import pytest

from src.services.hybrid_signal import determine_fundamental_zone, resolve_final_signal
from src.valuation.engine import ValuationEngine
from src.valuation.models import (
    FinalSignal,
    FundamentalZone,
    TechnicalState,
)


@pytest.fixture
def zones():
    return ValuationEngine.calculate_valuation_zones(26.30)


@pytest.mark.parametrize(
    "price,expected",
    [
        (20.0, FundamentalZone.UNDERVALUED),
        (26.30, FundamentalZone.UNDERVALUED),
        (28.0, FundamentalZone.FAIR),
        (30.24, FundamentalZone.FAIR),
        (31.0, FundamentalZone.OVERVALUED),
        (60.0, FundamentalZone.BUBBLE),
    ],
)
def test_fundamental_zone(price, expected, zones):
    assert determine_fundamental_zone(price, zones) == expected


@pytest.mark.parametrize(
    "fundamental,technical,signal,action",
    [
        (
            FundamentalZone.UNDERVALUED,
            TechnicalState.FISH_HEAD,
            FinalSignal.STRONG_BUY,
            "Immediate Entry",
        ),
        (
            FundamentalZone.UNDERVALUED,
            TechnicalState.FISH_BODY,
            FinalSignal.ADD_HOLD,
            "Accumulate",
        ),
        (
            FundamentalZone.FAIR,
            TechnicalState.FISH_HEAD,
            FinalSignal.BUY,
            "Strategic Entry",
        ),
        (
            FundamentalZone.FAIR,
            TechnicalState.FISH_BODY,
            FinalSignal.HOLD,
            "Maintain Position",
        ),
        (
            FundamentalZone.OVERVALUED,
            TechnicalState.FISH_BODY,
            FinalSignal.TIGHT_STOP,
            "Raise Stop-loss",
        ),
        (
            FundamentalZone.OVERVALUED,
            TechnicalState.FISH_TAIL,
            FinalSignal.STRONG_SELL,
            "Take Profit",
        ),
    ],
)
def test_truth_table_mappings(fundamental, technical, signal, action):
    result = resolve_final_signal(fundamental, technical)
    assert result is not None
    assert result[0] == signal
    assert result[1] == action


def test_bubble_any_state_strong_sell(zones):
    for tech in TechnicalState:
        sig, action = resolve_final_signal(FundamentalZone.BUBBLE, tech)
        assert sig == FinalSignal.STRONG_SELL
        assert action == "Full Exit"


def test_bone_broken_any_zone_exit(zones):
    for fund in FundamentalZone:
        if fund == FundamentalZone.BUBBLE:
            continue
        sig, action = resolve_final_signal(fund, TechnicalState.BONE_BROKEN)
        assert sig == FinalSignal.EXIT
        assert action == "Immediate Stop-out"
