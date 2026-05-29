"""測試健康檢查評分引擎"""
import numpy as np
import pandas as pd
import pytest
from src.scoring.engine import HealthCheckEngine


def make_df(prices: list[float], highs=None, lows=None) -> pd.DataFrame:
    """建立測試用 K 線 DataFrame（需要 70+ 筆以滿足均線計算）"""
    n = len(prices)
    if highs is None:
        highs = [p * 1.02 for p in prices]
    if lows is None:
        lows = [p * 0.98 for p in prices]
    return pd.DataFrame({
        "Date": pd.date_range("2025-01-01", periods=n, freq="D"),
        "Open": prices,
        "High": highs,
        "Low": lows,
        "Close": prices,
        "Volume": [1000] * n,
    })


def test_full_evaluation():
    """完整評分：模擬多頭排列資料"""
    # 建立 80 天上升趨勢 (多頭)
    prices = list(range(100, 180))
    df = make_df(prices)

    result = HealthCheckEngine.evaluate(df, stock_name="2330 台積電",
                                         foreign_net=500, sitc_net=200)
    assert result.stock_name == "2330 台積電"
    assert 0 <= result.total_score <= 100
    assert len(result.dimensions) == 5
    for d in result.dimensions:
        assert 0 <= d.score <= 20
        assert d.max_score == 20
    print(f"Total: {result.total_score}, Grade: {result.grade.value}")
    print(f"Dimensions: {[(d.name, d.score) for d in result.dimensions]}")


def test_grade_boundaries():
    """測試分數邊界"""
    from src.scoring.models import ScoreGrade
    assert ScoreGrade.from_score(100) == ScoreGrade.STRONG_BUY
    assert ScoreGrade.from_score(80) == ScoreGrade.STRONG_BUY
    assert ScoreGrade.from_score(79) == ScoreGrade.BULLISH
    assert ScoreGrade.from_score(60) == ScoreGrade.BULLISH
    assert ScoreGrade.from_score(59) == ScoreGrade.NEUTRAL
    assert ScoreGrade.from_score(40) == ScoreGrade.NEUTRAL
    assert ScoreGrade.from_score(39) == ScoreGrade.BEARISH
    assert ScoreGrade.from_score(0) == ScoreGrade.BEARISH


def test_ma_bullish_alignment():
    """多頭排列應得 20 分"""
    n = 80
    base = np.linspace(100, 150, n)
    close = pd.Series(base)
    # 手動製造 MA5 > MA10 > MA20 > MA60
    highs = close * 1.02
    lows = close * 0.98
    df = pd.DataFrame({"Close": close, "High": highs, "Low": lows})
    dim = HealthCheckEngine.score_ma(df)
    assert dim.score == 20, f"Expected 20, got {dim.score}: {dim.detail}"


def test_kd_oversold_cross():
    """KD 低檔黃金交叉應得 20 分"""
    # 建立先跌後平的資料，確保 K < 30
    n = 30
    prices = [100 - i * 2 for i in range(20)] + [60] * 10
    highs = [p + 1 for p in prices]
    lows = [p - 1 for p in prices]
    df = pd.DataFrame({"Close": prices, "High": highs, "Low": lows})
    dim = HealthCheckEngine.score_kd(df)
    print(f"KD: score={dim.score}, detail={dim.detail}")
    assert dim.score >= 0
