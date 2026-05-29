"""健康檢查評分模型"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ScoreGrade(str, Enum):
    STRONG_BUY = "🚀 強力利多（強烈建議入手）"
    BULLISH = "📈 偏多看好（可逢低布局）"
    NEUTRAL = "⚖️ 區間震盪（觀望為主）"
    BEARISH = "🚨 趨勢轉空（建議停損或賣掉）"

    @classmethod
    def from_score(cls, score: int) -> "ScoreGrade":
        if score >= 80:
            return cls.STRONG_BUY
        if score >= 60:
            return cls.BULLISH
        if score >= 40:
            return cls.NEUTRAL
        return cls.BEARISH


@dataclass
class DimensionScore:
    name: str          # MA / KD / MACD / RSI / 籌碼
    score: int         # 0-20
    max_score: int     # 20
    detail: str        # e.g. "多頭排列 MA5>MA10>MA20>MA60"


@dataclass
class HealthCheckResult:
    symbol: str
    stock_name: str
    total_score: int
    grade: ScoreGrade
    dimensions: List[DimensionScore] = field(default_factory=list)
    suggestion: str = ""
    updated_at: str = ""
