"""
Valuation Engine: Net Value recursion, Fish-Bone zones, and Hybrid Signal Matrix.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .models import (
    FinancialQuarterly,
    FundamentalZone,
    HybridSignal,
    HybridSignalResult,
    QuarterlyGridCell,
    TechnicalState,
    TechnicalStateResult,
    ValuationApiResponse,
    ValuationResult,
    ValuationZone,
    ValuationZoneLevels,
)


# ---------------------------------------------------------------------------
# Fundamental: Net Value recursion
# ---------------------------------------------------------------------------

def compute_net_value(
    records: List[FinancialQuarterly],
    initial_net_value: float = 0.0,
) -> List[QuarterlyGridCell]:
    """
    Build cumulative Net Value grid from quarterly financial data.
    Recursive Formula: NetValue_t = NetValue_{t-1} + (EPS_t + OCI_t + Other_t + Dividends_t + Adjustment_t)
    """
    net_value = initial_net_value
    grid: List[QuarterlyGridCell] = []
    for r in records:
        net_value = (
            net_value
            + r.eps
            + r.oci
            + r.other_items
            + r.dividends
            + r.adjustment_amount
        )
        grid.append(
            QuarterlyGridCell(
                year=r.year,
                quarter=r.quarter,
                eps=r.eps,
                oci=r.oci,
                other_items=r.other_items,
                dividends=r.dividends,
                adjustment_amount=r.adjustment_amount,
                accumulated_net_value=net_value,
            )
        )
    return grid


def compute_zones(net_value: float) -> ValuationZoneLevels:
    """
    Derive Fish-Bone price zones from the net_value baseline.
    Multipliers: Head (0.85x), Body (1.00x), Tail Low (1.15x), Tail High (1.30x), Bone (2.00x)
    """
    return ValuationZoneLevels(
        fish_head=round(net_value * 0.85, 4),
        fish_body=round(net_value * 1.00, 4),
        fish_tail_low=round(net_value * 1.15, 4),
        fish_tail_high=round(net_value * 1.30, 4),
        fish_bone=round(net_value * 2.00, 4),
    )


def determine_fundamental_zone(price: float, zones: ValuationZoneLevels) -> Tuple[FundamentalZone, ValuationZone]:
    """
    Map current price to a FundamentalZone and a specific ValuationZone.
    """
    if price >= zones.fish_bone:
        return FundamentalZone.BUBBLE, ValuationZone.FISH_BONE
    if price >= zones.fish_tail_high:
        return FundamentalZone.OVERVALUED, ValuationZone.FISH_TAIL_HIGH
    if price >= zones.fish_tail_low:
        return FundamentalZone.OVERVALUED, ValuationZone.FISH_TAIL_LOW
    if price >= zones.fish_body:
        return FundamentalZone.FAIR, ValuationZone.FISH_BODY
    return FundamentalZone.UNDERVALUED, ValuationZone.FISH_HEAD


# ---------------------------------------------------------------------------
# Technical indicators (pure-Python)
# ---------------------------------------------------------------------------

def _sma(prices: List[float], period: int) -> List[float]:
    """Simple moving average; pre-period values are 0.0."""
    result: List[float] = []
    for i in range(len(prices)):
        if i < period - 1:
            result.append(0.0)
        else:
            result.append(sum(prices[i - period + 1 : i + 1]) / period)
    return result


def _ema(prices: List[float], period: int) -> List[float]:
    """Exponential moving average with multiplier k = 2 / (period + 1)."""
    k = 2.0 / (period + 1)
    result: List[float] = []
    for i, p in enumerate(prices):
        if i == 0:
            result.append(p)
        else:
            result.append(p * k + result[-1] * (1.0 - k))
    return result


def _macd(prices: List[float]) -> Tuple[List[float], List[float], List[float]]:
    """Return (macd_line, signal_line, histogram) using standard 12/26/9 parameters."""
    ema12 = _ema(prices, 12)
    ema26 = _ema(prices, 26)
    macd_line = [a - b for a, b in zip(ema12, ema26)]
    signal_line = _ema(macd_line, 9)
    histogram = [a - b for a, b in zip(macd_line, signal_line)]
    return macd_line, signal_line, histogram


def _wilder_smooth(data: List[float], period: int) -> List[float]:
    """Wilder's smoothing method (used internally by ADX)."""
    n = len(data)
    out: List[float] = [0.0] * n
    if n > period:
        out[period] = sum(data[1 : period + 1])
        for i in range(period + 1, n):
            out[i] = out[i - 1] - out[i - 1] / period + data[i]
    return out


def _adx(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[float]:
    """Wilder-smoothed ADX series."""
    n = len(closes)
    if n < period + 1:
        return [0.0] * n

    tr_list: List[float] = [0.0]
    pdm_list: List[float] = [0.0]
    ndm_list: List[float] = [0.0]

    for i in range(1, n):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        up_move = highs[i] - highs[i - 1]
        down_move = lows[i - 1] - lows[i]
        pdm_list.append(up_move if up_move > down_move and up_move > 0 else 0.0)
        ndm_list.append(down_move if down_move > up_move and down_move > 0 else 0.0)
        tr_list.append(tr)

    atr = _wilder_smooth(tr_list, period)
    pdm_s = _wilder_smooth(pdm_list, period)
    ndm_s = _wilder_smooth(ndm_list, period)

    dx: List[float] = []
    for i in range(n):
        if atr[i] == 0.0:
            dx.append(0.0)
        else:
            dip = 100.0 * pdm_s[i] / atr[i]
            dim = 100.0 * ndm_s[i] / atr[i]
            denom = dip + dim
            dx.append(100.0 * abs(dip - dim) / denom if denom != 0.0 else 0.0)

    raw_adx = _wilder_smooth(dx, period)
    adx_out: List[float] = []
    for i in range(n):
        if i < period * 2:
            adx_out.append(0.0)
        else:
            adx_out.append(raw_adx[i] / period)
    return adx_out


# ---------------------------------------------------------------------------
# Technical state classifier
# ---------------------------------------------------------------------------

_BIAS_THRESHOLD: float = 15.0  # %
_ADX_THRESHOLD: float = 25.0


def classify_technical_state(
    closes: List[float],
    highs: Optional[List[float]] = None,
    lows: Optional[List[float]] = None,
) -> TechnicalStateResult:
    """
    Classify market state using MA5/10/20/60, MACD, ADX, and BIAS20.
    Returns a TechnicalStateResult.
    """
    if len(closes) < 60:
        raise ValueError("At least 60 closing prices are required for technical analysis.")

    _highs = highs if highs is not None else closes
    _lows = lows if lows is not None else closes

    price = closes[-1]
    ma5 = _sma(closes, 5)[-1]
    ma10 = _sma(closes, 10)[-1]
    ma20_series = _sma(closes, 20)
    ma60_series = _sma(closes, 60)

    ma20 = ma20_series[-1]
    ma60 = ma60_series[-1]

    bias20 = (price - ma20) / ma20 * 100.0 if ma20 != 0.0 else 0.0
    adx_series = _adx(_highs, _lows, closes)
    adx = adx_series[-1]

    macd_line, signal_line, _ = _macd(closes)

    # Determination logic for TechnicalState
    if bias20 > _BIAS_THRESHOLD:
        state = TechnicalState.OVEREXTENDED
    elif ma5 > ma10 and macd_line[-1] > signal_line[-1]:
        state = TechnicalState.FISH_HEAD
    elif price < ma20:
        state = TechnicalState.BEARISH
    elif price > ma20 and ma20 > ma60 and adx > _ADX_THRESHOLD:
        state = TechnicalState.BULLISH
    else:
        state = TechnicalState.NEUTRAL

    return TechnicalStateResult(
        state=state,
        fish_bone_value=round(ma20, 4),
        bias=round(bias20, 4),
        adx=round(adx, 4),
    )


# ---------------------------------------------------------------------------
# Hybrid Signal Matrix
# ---------------------------------------------------------------------------

# Matrix mapping (FundamentalZone, TechnicalState) -> (HybridSignal, action_description)
_SIGNAL_MATRIX: Dict[
    Tuple[FundamentalZone, TechnicalState],
    Tuple[HybridSignal, str],
] = {
    # UNDERVALUED
    (FundamentalZone.UNDERVALUED, TechnicalState.BULLISH):      (HybridSignal.STRONG_BUY, "Deep value with strong trend confirmation. Maximize position."),
    (FundamentalZone.UNDERVALUED, TechnicalState.NEUTRAL):      (HybridSignal.BUY,        "Deep value, awaiting trend. Accumulate slowly."),
    (FundamentalZone.UNDERVALUED, TechnicalState.BEARISH):      (HybridSignal.HOLD,       "Deep value but technicals broken. Hold/Wait for bottom."),
    (FundamentalZone.UNDERVALUED, TechnicalState.OVEREXTENDED): (HybridSignal.BUY,        "Deep value but short-term overextended. Buy on dips."),

    # FAIR
    (FundamentalZone.FAIR, TechnicalState.BULLISH):      (HybridSignal.BUY,        "Fair value with positive momentum. Suitable entry."),
    (FundamentalZone.FAIR, TechnicalState.NEUTRAL):      (HybridSignal.HOLD,       "Fair value, neutral trend. Maintain position."),
    (FundamentalZone.FAIR, TechnicalState.BEARISH):      (HybridSignal.SELL,       "Fair value but trend broken. Reduce exposure."),
    (FundamentalZone.FAIR, TechnicalState.OVEREXTENDED): (HybridSignal.HOLD,       "Fair value but overextended. Hold, do not add."),

    # OVERVALUED
    (FundamentalZone.OVERVALUED, TechnicalState.BULLISH):      (HybridSignal.HOLD,       "Overvalued but trend is strong. Hold with tight stops."),
    (FundamentalZone.OVERVALUED, TechnicalState.NEUTRAL):      (HybridSignal.SELL,       "Overvalued and trend stalling. Start exiting."),
    (FundamentalZone.OVERVALUED, TechnicalState.BEARISH):      (HybridSignal.STRONG_SELL, "Overvalued and trend broken. Exit quickly."),
    (FundamentalZone.OVERVALUED, TechnicalState.OVEREXTENDED): (HybridSignal.STRONG_SELL, "Overvalued and overextended. High risk of correction."),

    # BUBBLE
    (FundamentalZone.BUBBLE, TechnicalState.BULLISH):      (HybridSignal.SELL,       "Bubble territory. Trend is strong but risk is extreme."),
    (FundamentalZone.BUBBLE, TechnicalState.NEUTRAL):      (HybridSignal.STRONG_SELL, "Bubble territory, momentum fading. Exit."),
    (FundamentalZone.BUBBLE, TechnicalState.BEARISH):      (HybridSignal.STRONG_SELL, "Bubble collapsing. Immediate exit."),
    (FundamentalZone.BUBBLE, TechnicalState.OVEREXTENDED): (HybridSignal.STRONG_SELL, "Extreme bubble and overextended. Immediate exit."),
}


def determine_signal(
    fundamental_zone: FundamentalZone,
    technical_state: TechnicalState,
) -> Tuple[HybridSignal, str]:
    """
    Return (HybridSignal, action_description) from the Hybrid Signal Matrix.
    """
    return _SIGNAL_MATRIX.get(
        (fundamental_zone, technical_state),
        (HybridSignal.HOLD, "No specific signal match; maintain neutral stance.")
    )


# ---------------------------------------------------------------------------
# Top-level orchestrators
# ---------------------------------------------------------------------------

def run_valuation(
    symbol: str,
    price: float,
    records: List[FinancialQuarterly],
    closes: List[float],
    highs: Optional[List[float]] = None,
    lows: Optional[List[float]] = None,
    initial_net_value: float = 0.0,
) -> HybridSignalResult:
    """
    Full pipeline: fundamental + technical -> hybrid signal.
    """
    grid = compute_net_value(records, initial_net_value)
    net_value = grid[-1].accumulated_net_value if grid else initial_net_value
    zones = compute_zones(net_value)
    fundamental_zone, current_zone = determine_fundamental_zone(price, zones)
    technical = classify_technical_state(closes, highs, lows)
    final_signal, action = determine_signal(fundamental_zone, technical.state)

    return HybridSignalResult(
        symbol=symbol,
        fundamental_zone=fundamental_zone,
        technical_state=technical.state,
        final_signal=final_signal,
        action=action,
        valuation=ValuationResult(
            symbol=symbol,
            price=price,
            net_value=net_value,
            zones=zones,
            current_zone=current_zone,
        ),
        technical=technical,
    )


def build_api_response(
    symbol: str,
    price: float,
    records: List[FinancialQuarterly],
    closes: List[float],
    highs: Optional[List[float]] = None,
    lows: Optional[List[float]] = None,
    initial_net_value: float = 0.0,
) -> ValuationApiResponse:
    """
    Build the full ValuationApiResponse including quarterly grid for the API layer.
    """
    grid = compute_net_value(records, initial_net_value)
    net_value = grid[-1].accumulated_net_value if grid else initial_net_value
    zones = compute_zones(net_value)
    fundamental_zone, current_zone = determine_fundamental_zone(price, zones)

    return ValuationApiResponse(
        valuation=ValuationResult(
            symbol=symbol,
            price=price,
            net_value=net_value,
            zones=zones,
            current_zone=current_zone,
        ),
        quarterly_grid=grid,
        fundamental_zone=fundamental_zone,
    )
