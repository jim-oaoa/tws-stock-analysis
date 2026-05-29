"""健康檢查評分引擎 — 5 維度各 20 分，總分 100"""

from datetime import datetime, timezone
from typing import Optional

import numpy as np
import pandas as pd

from src.scoring.models import DimensionScore, HealthCheckResult, ScoreGrade


class HealthCheckEngine:
    """一鍵健檢評分引擎"""

    @staticmethod
    def _sma(series: pd.Series, window: int) -> pd.Series:
        return series.rolling(window=window, min_periods=window).mean()

    @staticmethod
    def _ema(series: pd.Series, span: int) -> pd.Series:
        return series.ewm(span=span, adjust=False).mean()

    @staticmethod
    def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
        """計算 RSI"""
        delta = close.diff()
        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)
        avg_gain = gain.rolling(period, min_periods=period).mean()
        avg_loss = loss.rolling(period, min_periods=period).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        return 100 - (100 / (1 + rs))

    @staticmethod
    def _kd(close: pd.Series, high: pd.Series, low: pd.Series,
            n: int = 9) -> tuple[pd.Series, pd.Series]:
        """計算 KD 指標，回傳 (K, D)"""
        lowest_low = low.rolling(n, min_periods=n).min()
        highest_high = high.rolling(n, min_periods=n).max()
        rsv = (close - lowest_low) / (highest_high - lowest_low).replace(0, np.nan) * 100
        k = rsv.ewm(com=2, adjust=False).mean()
        d = k.ewm(com=2, adjust=False).mean()
        return k, d

    @classmethod
    def score_ma(cls, df: pd.DataFrame) -> DimensionScore:
        """均線評分 (20 分)"""
        close = df["Close"]
        ma5 = cls._sma(close, 5)
        ma10 = cls._sma(close, 10)
        ma20 = cls._sma(close, 20)
        ma60 = cls._sma(close, 60)

        idx = len(close) - 1
        cur = close.iloc[idx]
        m5, m10, m20, m60 = ma5.iloc[idx], ma10.iloc[idx], ma20.iloc[idx], ma60.iloc[idx]

        # 多頭排列
        if not any(np.isnan(x) for x in [m5, m10, m20, m60]):
            if m5 > m10 > m20 > m60:
                return DimensionScore("MA 均線", 20, 20, "多頭排列 MA5>MA10>MA20>MA60")

        # 跌破月線
        if not np.isnan(m20) and cur < m20:
            return DimensionScore("MA 均線", 0, 20, "跌破月線 Close < MA20")

        # 黃金交叉 (MA5 上穿 MA20)
        if idx > 0 and not any(np.isnan(x) for x in [m5, m20]):
            prev_m5 = ma5.iloc[idx - 1]
            prev_m20 = ma20.iloc[idx - 1]
            if prev_m5 <= prev_m20 and m5 > m20:
                return DimensionScore("MA 均線", 15, 20, "黃金交叉 MA5 上穿 MA20")

        return DimensionScore("MA 均線", 5, 20, "盤整（站上月線但未多頭排列）")

    @classmethod
    def score_kd(cls, df: pd.DataFrame) -> DimensionScore:
        """KD 指標評分 (20 分)"""
        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        k, d = cls._kd(close, high, low)

        idx = len(close) - 1
        cur_k, cur_d = k.iloc[idx], d.iloc[idx]

        if np.isnan(cur_k) or np.isnan(cur_d):
            return DimensionScore("KD 指標", 10, 20, "資料不足，預設中性")

        # 低檔黃金交叉
        if idx > 0:
            prev_k, prev_d = k.iloc[idx - 1], d.iloc[idx - 1]
            if not np.isnan(prev_k) and not np.isnan(prev_d):
                if cur_k < 30 and prev_k <= prev_d and cur_k > cur_d:
                    return DimensionScore("KD 指標", 20, 20, f"低檔黃金交叉 K={cur_k:.1f}")

        # 高檔死亡交叉
        if idx > 0:
            prev_k, prev_d = k.iloc[idx - 1], d.iloc[idx - 1]
            if not np.isnan(prev_k) and not np.isnan(prev_d):
                if cur_k > 80 and prev_k >= prev_d and cur_k < cur_d:
                    return DimensionScore("KD 指標", 0, 20, f"高檔死亡交叉 K={cur_k:.1f}")

        return DimensionScore("KD 指標", 10, 20, f"中性區間 K={cur_k:.1f}")

    @classmethod
    def score_macd(cls, df: pd.DataFrame) -> DimensionScore:
        """MACD 評分 (20 分)"""
        close = df["Close"]
        ema12 = cls._ema(close, 12)
        ema26 = cls._ema(close, 26)
        dif = ema12 - ema26
        dea = cls._ema(dif, 9)
        macd_bar = (dif - dea) * 2  # 柱狀體

        idx = len(close) - 1
        cur_bar = macd_bar.iloc[idx]
        cur_dif = dif.iloc[idx]

        if np.isnan(cur_bar):
            return DimensionScore("MACD", 10, 20, "資料不足，預設中性")

        if idx > 0:
            prev_bar = macd_bar.iloc[idx - 1]
            if np.isnan(prev_bar):
                return DimensionScore("MACD", 10, 20, "資料不足")

            # DIFF > 0: 紅柱區域
            if cur_dif > 0:
                if cur_bar > prev_bar:
                    return DimensionScore("MACD", 20, 20, "紅柱增長，動能增強")
                else:
                    return DimensionScore("MACD", 5, 20, "紅柱遞減，動能減弱")
            # DIFF < 0: 綠柱區域
            else:
                if cur_bar > prev_bar:
                    return DimensionScore("MACD", 10, 20, "綠柱收斂，賣壓減輕")
                else:
                    return DimensionScore("MACD", 0, 20, "綠柱增長，賣壓加重")

        return DimensionScore("MACD", 10, 20, "中性")

    @classmethod
    def score_rsi(cls, df: pd.DataFrame) -> DimensionScore:
        """RSI 評分 (20 分)"""
        close = df["Close"]
        rsi = cls._rsi(close, 14)

        idx = len(close) - 1
        cur_rsi = rsi.iloc[idx]

        if np.isnan(cur_rsi):
            return DimensionScore("RSI", 10, 20, "資料不足")

        # 超賣反轉
        if idx > 0:
            prev_rsi = rsi.iloc[idx - 1]
            if not np.isnan(prev_rsi) and cur_rsi < 30 and cur_rsi > prev_rsi:
                return DimensionScore("RSI", 20, 20, f"超賣反轉 RSI={cur_rsi:.1f}")

        if cur_rsi > 70:
            return DimensionScore("RSI", 0, 20, f"過熱 RSI={cur_rsi:.1f}")

        return DimensionScore("RSI", 10, 20, f"中性 RSI={cur_rsi:.1f}")

    @classmethod
    def score_institutional(cls, foreign_net: Optional[float] = None,
                            sitc_net: Optional[float] = None) -> DimensionScore:
        """籌碼加權評分 (20 分)"""
        if foreign_net is None and sitc_net is None:
            return DimensionScore("籌碼加權", 5, 20, "無三大法人資料")

        f_buy = foreign_net is not None and foreign_net > 0
        s_buy = sitc_net is not None and sitc_net > 0
        f_sell = foreign_net is not None and foreign_net < 0
        s_sell = sitc_net is not None and sitc_net < 0

        if f_buy and s_buy:
            return DimensionScore("籌碼加權", 20, 20, "外資+投信同步買超")
        if f_buy or s_buy:
            detail = []
            if f_buy: detail.append(f"外資買超 {foreign_net:+.0f}")
            if s_buy: detail.append(f"投信買超 {sitc_net:+.0f}")
            return DimensionScore("籌碼加權", 10, 20, "僅一方買超 " + ", ".join(detail))
        if f_sell and s_sell:
            return DimensionScore("籌碼加權", 0, 20, "外資+投信同步賣超")

        return DimensionScore("籌碼加權", 5, 20, "買賣互見，方向不明")

    @classmethod
    def evaluate(cls, df: pd.DataFrame, stock_name: str = "",
                 foreign_net: Optional[float] = None,
                 sitc_net: Optional[float] = None) -> HealthCheckResult:
        """執行完整健檢評分"""
        symbol = stock_name  # fallback
        dims = [
            cls.score_ma(df),
            cls.score_kd(df),
            cls.score_macd(df),
            cls.score_rsi(df),
            cls.score_institutional(foreign_net, sitc_net),
        ]
        total = sum(d.score for d in dims)
        grade = ScoreGrade.from_score(total)

        suggestions = {
            ScoreGrade.STRONG_BUY: "各項指標一致偏多，建議積極布局，分批進場。",
            ScoreGrade.BULLISH: "整體偏多但仍有觀望信號，可逢拉回布局，控制部位。",
            ScoreGrade.NEUTRAL: "多空交戰方向不明，建議觀望等待趨勢確立後再進場。",
            ScoreGrade.BEARISH: "多項指標轉空，建議減碼或停損，保留現金等待落底。",
        }

        return HealthCheckResult(
            symbol=symbol,
            stock_name=stock_name,
            total_score=total,
            grade=grade,
            dimensions=dims,
            suggestion=suggestions.get(grade, ""),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
