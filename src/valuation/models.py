"""
Valuation Engine Data Models: Enums and Pydantic BaseModels for the Fish-Bone Valuation Model.
"""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ValuationZone(str, Enum):
    """Specific zones of the Fish-Bone model based on multipliers."""
    FISH_HEAD = "FISH_HEAD"           # Undervalued (0.85x)
    FISH_BODY = "FISH_BODY"           # Fair Value (1.00x)
    FISH_TAIL_LOW = "FISH_TAIL_LOW"   # Slightly Overvalued (1.15x)
    FISH_TAIL_HIGH = "FISH_TAIL_HIGH" # Overvalued (1.30x)
    FISH_BONE = "FISH_BONE"           # Critical Support/Resistance (2.00x)


class FundamentalZone(str, Enum):
    """General fundamental valuation categories."""
    UNDERVALUED = "UNDERVALUED"
    FAIR = "FAIR"
    OVERVALUED = "OVERVALUED"
    BUBBLE = "BUBBLE"


class TechnicalState(str, Enum):
    """Technical market state based on indicators (Trend, Momentum, Strength)."""
    FISH_HEAD = "FISH_HEAD"       # High momentum (MA5 > MA10 & MACD Golden Cross)
    BULLISH = "BULLISH"
    NEUTRAL = "NEUTRAL"
    BEARISH = "BEARISH"
    OVEREXTENDED = "OVEREXTENDED"


class HybridSignal(str, Enum):
    """Final signal derived from the intersection of Fundamental Zone and Technical State."""
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"


# ---------------------------------------------------------------------------
# Financial Input Models
# ---------------------------------------------------------------------------

class FinancialQuarterly(BaseModel):
    """Input data for a single financial quarter."""
    symbol: str
    year: int
    quarter: int
    eps: float = Field(..., description="Earnings Per Share")
    oci: float = Field(..., description="Other Comprehensive Income")
    other_items: float = Field(..., description="Other adjustments")
    dividends: float = Field(..., description="Dividends paid")
    adjustment_amount: float = Field(..., description="One-time adjustments")


# ---------------------------------------------------------------------------
# Valuation Output Models
# ---------------------------------------------------------------------------

class ValuationZoneLevels(BaseModel):
    """Absolute price levels for each Fish-Bone zone, derived from net_value baseline."""
    fish_head: float       # 0.85x baseline
    fish_body: float       # 1.00x baseline
    fish_tail_low: float   # 1.15x baseline
    fish_tail_high: float  # 1.30x baseline
    fish_bone: float       # 2.00x baseline


class ValuationResult(BaseModel):
    """The result of the fundamental valuation engine."""
    symbol: str
    price: float
    net_value: float            # Latest accumulated baseline
    zones: ValuationZoneLevels
    current_zone: ValuationZone


# ---------------------------------------------------------------------------
# Technical Analysis Models
# ---------------------------------------------------------------------------

class TechnicalStateResult(BaseModel):
    """The result of the technical analysis engine."""
    state: TechnicalState
    fish_bone_value: float  # e.g., MA20
    bias: float             # BIAS20 (%)
    adx: float              # Trend strength


# ---------------------------------------------------------------------------
# Quarterly Grid Models
# ---------------------------------------------------------------------------

class QuarterlyGridCell(BaseModel):
    """A single cell in the recursive net value calculation grid."""
    year: int
    quarter: int
    eps: float
    oci: float
    other_items: float
    dividends: float
    adjustment_amount: float
    accumulated_net_value: float


# ---------------------------------------------------------------------------
# API Response Models
# ---------------------------------------------------------------------------

class ValuationApiResponse(BaseModel):
    """Full API response for a stock valuation request."""
    valuation: ValuationResult
    quarterly_grid: List[QuarterlyGridCell]
    fundamental_zone: FundamentalZone


class HybridSignalResult(BaseModel):
    """Full response for the hybrid technical-fundamental signal."""
    symbol: str
    fundamental_zone: FundamentalZone
    technical_state: TechnicalState
    final_signal: HybridSignal
    action: str
    valuation: ValuationResult
    technical: TechnicalStateResult
