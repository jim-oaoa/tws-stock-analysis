"""
混合信號服務：ValuationEngine × TechnicalAnalysis → CURSOR_IMPLEMENTATION_GUIDE Truth Table
"""

from typing import Dict, List, Optional, Tuple

import pandas as pd

from src.technical.analysis import TechnicalAnalysis
from src.valuation.engine import ValuationEngine
from src.valuation.models import (
    FinalSignal,
    FinancialQuarterly,
    FundamentalZone,
    HybridSignalResult,
    QuarterlyGridCell,
    TechnicalState,
    TechnicalStateResult,
    ValuationApiResponse,
    ValuationZoneLevels,
)

# Section 3 Truth Table（嚴格對照 CURSOR_IMPLEMENTATION_GUIDE）
_TRUTH_TABLE: Dict[Tuple[FundamentalZone, TechnicalState], Tuple[FinalSignal, str]] = {
    (FundamentalZone.UNDERVALUED, TechnicalState.FISH_HEAD): (
        FinalSignal.STRONG_BUY,
        "Immediate Entry",
    ),
    (FundamentalZone.UNDERVALUED, TechnicalState.FISH_BODY): (
        FinalSignal.ADD_HOLD,
        "Accumulate",
    ),
    (FundamentalZone.FAIR, TechnicalState.FISH_HEAD): (
        FinalSignal.BUY,
        "Strategic Entry",
    ),
    (FundamentalZone.FAIR, TechnicalState.FISH_BODY): (
        FinalSignal.HOLD,
        "Maintain Position",
    ),
    (FundamentalZone.OVERVALUED, TechnicalState.FISH_BODY): (
        FinalSignal.TIGHT_STOP,
        "Raise Stop-loss",
    ),
    (FundamentalZone.OVERVALUED, TechnicalState.FISH_TAIL): (
        FinalSignal.STRONG_SELL,
        "Take Profit",
    ),
}


def determine_fundamental_zone(price: float, zones: ValuationZoneLevels) -> FundamentalZone:
    """基本面區間（依 fish-bone-valuation-logic.md Dimension A）。"""
    if price >= zones.fish_bone:
        return FundamentalZone.BUBBLE
    if price <= zones.fish_body:
        return FundamentalZone.UNDERVALUED
    if price <= zones.fish_tail_low:
        return FundamentalZone.FAIR
    return FundamentalZone.OVERVALUED


def resolve_final_signal(
    fundamental: FundamentalZone,
    technical: TechnicalState,
) -> Optional[Tuple[FinalSignal, str]]:
    """
    Truth Table 解析：
    - BUBBLE + ANY → STRONG SELL
    - ANY + BONE_BROKEN → EXIT
    - 其餘查表
    """
    if fundamental == FundamentalZone.BUBBLE:
        return FinalSignal.STRONG_SELL, "Full Exit"
    if technical == TechnicalState.BONE_BROKEN:
        return FinalSignal.EXIT, "Immediate Stop-out"
    return _TRUTH_TABLE.get((fundamental, technical))


def build_quarterly_grid(
    financials: List[FinancialQuarterly],
    initial_net_value: float,
) -> List[QuarterlyGridCell]:
    sorted_financials = sorted(financials, key=lambda x: (x.year, x.quarter))
    accumulated = ValuationEngine.calculate_accumulated_net_values(
        sorted_financials, initial_net_value
    )
    return [
        QuarterlyGridCell(
            year=f.year,
            quarter=f.quarter,
            eps=f.eps,
            oci=f.oci,
            other_items=f.other_items,
            dividends=f.dividends,
            adjustment_amount=f.adjustment_amount,
            accumulated_net_value=acc,
        )
        for f, acc in zip(sorted_financials, accumulated)
    ]


class HybridSignalService:
    """整合估值引擎與技術分析，輸出最終信號。"""

    @staticmethod
    def get_valuation(
        symbol: str,
        price: float,
        financials: List[FinancialQuarterly],
        initial_net_value: float,
    ) -> ValuationApiResponse:
        sorted_financials = sorted(financials, key=lambda x: (x.year, x.quarter))
        valuation = ValuationEngine.get_full_valuation_state(
            symbol=symbol,
            price=price,
            financials=sorted_financials,
            initial_net_value=initial_net_value,
        )
        fundamental = determine_fundamental_zone(price, valuation.zones)
        grid = build_quarterly_grid(sorted_financials, initial_net_value)
        return ValuationApiResponse(
            valuation=valuation,
            quarterly_grid=grid,
            fundamental_zone=fundamental,
        )

    @staticmethod
    def get_hybrid_signal(
        symbol: str,
        price: float,
        financials: List[FinancialQuarterly],
        initial_net_value: float,
        price_bars_df: pd.DataFrame,
    ) -> HybridSignalResult:
        valuation_resp = HybridSignalService.get_valuation(
            symbol, price, financials, initial_net_value
        )
        technical: TechnicalStateResult = TechnicalAnalysis(price_bars_df).evaluate()
        fundamental = valuation_resp.fundamental_zone

        resolved = resolve_final_signal(fundamental, technical.state)
        if resolved is None:
            raise ValueError(
                f"No Truth Table mapping for "
                f"{fundamental.value} × {technical.state.value}"
            )
        final_signal, action = resolved

        return HybridSignalResult(
            symbol=symbol,
            fundamental_zone=fundamental,
            technical_state=technical.state,
            final_signal=final_signal,
            action=action,
            valuation=valuation_resp.valuation,
            technical=technical,
        )
