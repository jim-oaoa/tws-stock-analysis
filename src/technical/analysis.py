"""
技術面分析（依 docs/skills/fish-bone-valuation-logic.md）。
評估順序：BONE_BROKEN → FISH_TAIL → FISH_BODY → FISH_HEAD
"""

from typing import Tuple

import numpy as np
import pandas as pd

from src.valuation.models import TechnicalState, TechnicalStateResult


class TechnicalAnalysis:
    """從標準化 K 線 DataFrame 判定技術狀態。"""

    def __init__(self, bars: pd.DataFrame):
        required = {"Date", "Open", "High", "Low", "Close", "Volume"}
        missing = required - set(bars.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        if bars.empty:
            raise ValueError("Price bars cannot be empty")
        self._df = bars.copy().reset_index(drop=True)

    @staticmethod
    def _sma(series: pd.Series, window: int) -> pd.Series:
        return series.rolling(window=window, min_periods=window).mean()

    @staticmethod
    def _ema(series: pd.Series, span: int) -> pd.Series:
        return series.ewm(span=span, adjust=False).mean()

    def _macd(self) -> Tuple[pd.Series, pd.Series]:
        close = self._df["Close"]
        ema12 = self._ema(close, 12)
        ema26 = self._ema(close, 26)
        macd_line = ema12 - ema26
        signal = self._ema(macd_line, 9)
        return macd_line, signal

    def _adx(self, period: int = 14) -> pd.Series:
        high = self._df["High"]
        low = self._df["Low"]
        close = self._df["Close"]
        prev_close = close.shift(1)
        tr = pd.concat(
            [
                high - low,
                (high - prev_close).abs(),
                (low - prev_close).abs(),
            ],
            axis=1,
        ).max(axis=1)
        up_move = high.diff()
        down_move = -low.diff()
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
        atr = tr.rolling(period, min_periods=period).mean()
        plus_di = 100 * pd.Series(plus_dm).rolling(period, min_periods=period).mean() / atr
        minus_di = 100 * pd.Series(minus_dm).rolling(period, min_periods=period).mean() / atr
        dx = (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan) * 100
        return dx.rolling(period, min_periods=period).mean()

    def evaluate(self) -> TechnicalStateResult:
        close = self._df["Close"]
        ma5 = self._sma(close, 5)
        ma10 = self._sma(close, 10)
        ma20 = self._sma(close, 20)
        ma60 = self._sma(close, 60)
        macd_line, macd_signal = self._macd()
        adx_series = self._adx()
        bias20 = (close - ma20) / ma20 * 100

        idx = len(close) - 1
        price = float(close.iloc[idx])
        ma20_val = float(ma20.iloc[idx])
        ma60_val = float(ma60.iloc[idx]) if not np.isnan(ma60.iloc[idx]) else 0.0
        adx_val = float(adx_series.iloc[idx]) if not np.isnan(adx_series.iloc[idx]) else 0.0
        bias_val = float(bias20.iloc[idx]) if not np.isnan(bias20.iloc[idx]) else 0.0

        prev_close = float(close.iloc[idx - 1]) if idx > 0 else price
        if idx > 0 and not np.isnan(ma20.iloc[idx - 1]):
            prev_ma20 = float(ma20.iloc[idx - 1])
        else:
            prev_ma20 = ma20_val

        # BONE_BROKEN: 收盤跌破 MA20 且未能 reclaim
        if price < ma20_val and prev_close < prev_ma20:
            state = TechnicalState.BONE_BROKEN
        elif bias_val > 15.0:
            # FISH_TAIL: BIAS_20 > 15%（高估延伸）
            state = TechnicalState.FISH_TAIL
        elif price > ma20_val > ma60_val and adx_val > 25.0:
            # FISH_BODY: 主趨勢
            state = TechnicalState.FISH_BODY
        else:
            golden_cross = (
                idx > 0
                and float(macd_line.iloc[idx]) > float(macd_signal.iloc[idx])
                and float(macd_line.iloc[idx - 1]) <= float(macd_signal.iloc[idx - 1])
            )
            if (
                price > float(ma5.iloc[idx])
                and price > float(ma10.iloc[idx])
                and golden_cross
            ):
                state = TechnicalState.FISH_HEAD
            else:
                state = TechnicalState.FISH_BODY

        return TechnicalStateResult(
            state=state,
            fish_bone_value=ma20_val,
            bias=bias_val,
            adx=adx_val,
        )
