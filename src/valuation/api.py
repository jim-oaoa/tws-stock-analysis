"""
Valuation API endpoints: FastAPI router wrapping build_api_response and run_valuation.
"""

from __future__ import annotations

import asyncio
import math
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from .engine import build_api_response, run_valuation
from .models import (
    FinancialQuarterly,
    HybridSignalResult,
    ValuationApiResponse,
)
from .repository import StockRepository

router = APIRouter(prefix="/valuation", tags=["valuation"])

_repo = StockRepository()


# ---------------------------------------------------------------------------
# Request body models
# ---------------------------------------------------------------------------

class ValuationRequest(BaseModel):
    symbol: str
    price: float = Field(..., gt=0, description="Current market price")
    records: List[FinancialQuarterly] = Field(..., min_length=1, description="Quarterly financial records")
    closes: List[float] = Field(..., min_length=60, description="Historical closing prices (min 60 required)")
    highs: Optional[List[float]] = Field(None, description="Historical high prices; length must match closes")
    lows: Optional[List[float]] = Field(None, description="Historical low prices; length must match closes")
    initial_net_value: float = Field(0.0, description="Starting net value for the recursive accumulation")


class SignalRequest(BaseModel):
    symbol: str
    price: float = Field(..., gt=0, description="Current market price")
    records: List[FinancialQuarterly] = Field(..., min_length=1, description="Quarterly financial records")
    closes: List[float] = Field(..., min_length=60, description="Historical closing prices (min 60 required)")
    highs: Optional[List[float]] = Field(None, description="Historical high prices; length must match closes")
    lows: Optional[List[float]] = Field(None, description="Historical low prices; length must match closes")
    initial_net_value: float = Field(0.0, description="Starting net value for the recursive accumulation")


# ---------------------------------------------------------------------------
# GET endpoints (auto-fetch via repository)
# ---------------------------------------------------------------------------

@router.get(
    "/signal/{symbol}",
    response_model=HybridSignalResult,
    summary="Fetch data and compute hybrid fundamental + technical signal",
)
async def get_signal(
    symbol: str,
    period: str = Query("1y", description="Price history period (e.g. '1y', '2y', 'max')"),
    initial_net_value: float = Query(0.0, description="Starting net value for the recursive accumulation"),
) -> HybridSignalResult:
    """
    Automatically fetch price series and financial records for a symbol via
    StockRepository, then run the full valuation + hybrid signal pipeline.
    """
    highs, lows, closes = await asyncio.to_thread(_repo.get_price_series, symbol, period)
    # Filter NaN values from yfinance data (occur when market is closed)
    closes = [float(v) for v in closes if not (isinstance(v, float) and math.isnan(v))]
    if highs:
        highs = [float(v) if not (isinstance(v, float) and math.isnan(v)) else 0.0 for v in highs]
    if lows:
        lows = [float(v) if not (isinstance(v, float) and math.isnan(v)) else 0.0 for v in lows]
    if not closes:
        raise HTTPException(status_code=404, detail=f"No price data found for symbol '{symbol}'.")
    if len(closes) < 60:
        raise HTTPException(
            status_code=422,
            detail=f"Insufficient price history for '{symbol}': {len(closes)} bars returned, 60 required.",
        )

    records = await asyncio.to_thread(_repo.get_financials, symbol)
    if not records:
        raise HTTPException(status_code=404, detail=f"No financial data found for symbol '{symbol}'.")

    price = float(closes[-1])
    closes = [float(v) for v in closes]
    highs = [float(v) for v in highs] if highs else None
    lows = [float(v) for v in lows] if lows else None
    highs_arg = highs if highs else None
    lows_arg = lows if lows else None

    try:
        return run_valuation(
            symbol=symbol,
            price=price,
            records=records,
            closes=closes,
            highs=highs_arg,
            lows=lows_arg,
            initial_net_value=initial_net_value,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Signal computation failed: {exc}") from exc


@router.get(
    "/{symbol}",
    response_model=ValuationApiResponse,
    summary="Fetch data and compute Fish-Bone valuation",
)
async def get_valuation(
    symbol: str,
    period: str = Query("1y", description="Price history period (e.g. '1y', '2y', 'max')"),
    initial_net_value: float = Query(0.0, description="Starting net value for the recursive accumulation"),
) -> ValuationApiResponse:
    """
    Automatically fetch price series and financial records for a symbol via
    StockRepository, then compute the Fish-Bone valuation grid and fundamental zone.
    """
    highs, lows, closes = await asyncio.to_thread(_repo.get_price_series, symbol, period)
    # Filter NaN values from yfinance data (occur when market is closed)
    closes = [float(v) for v in closes if not (isinstance(v, float) and math.isnan(v))]
    if highs:
        highs = [float(v) if not (isinstance(v, float) and math.isnan(v)) else 0.0 for v in highs]
    if lows:
        lows = [float(v) if not (isinstance(v, float) and math.isnan(v)) else 0.0 for v in lows]
    if not closes:
        raise HTTPException(status_code=404, detail=f"No price data found for symbol '{symbol}'.")
    if len(closes) < 60:
        raise HTTPException(
            status_code=422,
            detail=f"Insufficient price history for '{symbol}': {len(closes)} bars returned, 60 required.",
        )

    records = await asyncio.to_thread(_repo.get_financials, symbol)
    if not records:
        raise HTTPException(status_code=404, detail=f"No financial data found for symbol '{symbol}'.")

    price = float(closes[-1])
    closes = [float(v) for v in closes]
    highs = [float(v) for v in highs] if highs else None
    lows = [float(v) for v in lows] if lows else None
    highs_arg = highs if highs else None
    lows_arg = lows if lows else None

    try:
        return build_api_response(
            symbol=symbol,
            price=price,
            records=records,
            closes=closes,
            highs=highs_arg,
            lows=lows_arg,
            initial_net_value=initial_net_value,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Valuation computation failed: {exc}") from exc


# ---------------------------------------------------------------------------
# POST endpoints (manual / debug)
# ---------------------------------------------------------------------------

@router.post(
    "/",
    response_model=ValuationApiResponse,
    summary="Compute Fish-Bone valuation grid and fundamental zone",
)
async def post_valuation(req: ValuationRequest) -> ValuationApiResponse:
    """
    Compute Fish-Bone price zones and fundamental zone for a symbol.

    Returns the full quarterly net-value accumulation grid alongside all
    zone price levels (Head 0.85x → Bone 2.00x) and the current zone.
    """
    _validate_series_lengths(req.closes, req.highs, req.lows)
    try:
        return build_api_response(
            symbol=req.symbol,
            price=req.price,
            records=req.records,
            closes=req.closes,
            highs=req.highs,
            lows=req.lows,
            initial_net_value=req.initial_net_value,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Valuation computation failed: {exc}") from exc


@router.post(
    "/signal",
    response_model=HybridSignalResult,
    summary="Compute hybrid fundamental + technical signal",
)
async def post_signal(req: SignalRequest) -> HybridSignalResult:
    """
    Run the full valuation pipeline and return the Hybrid Signal.

    Combines Fish-Bone fundamental zone classification with technical state
    (MA20/60, BIAS20, ADX) through the Hybrid Signal Matrix to produce a
    final actionable signal: STRONG_BUY → STRONG_SELL.
    """
    _validate_series_lengths(req.closes, req.highs, req.lows)
    try:
        return run_valuation(
            symbol=req.symbol,
            price=req.price,
            records=req.records,
            closes=req.closes,
            highs=req.highs,
            lows=req.lows,
            initial_net_value=req.initial_net_value,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Signal computation failed: {exc}") from exc


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _validate_series_lengths(
    closes: List[float],
    highs: Optional[List[float]],
    lows: Optional[List[float]],
) -> None:
    """Raise HTTP 400 when optional highs/lows are provided with a mismatched length."""
    n = len(closes)
    if highs is not None and len(highs) != n:
        raise HTTPException(
            status_code=400,
            detail=(
                f"'highs' length {len(highs)} does not match 'closes' length {n}. "
                "All price series must have the same number of bars.",
            ),
        )
    if lows is not None and len(lows) != n:
        raise HTTPException(
            status_code=400,
            detail=(
                f"'lows' length {len(lows)} does not match 'closes' length {n}. "
                "All price series must have the same number of bars.",
            ),
        )
