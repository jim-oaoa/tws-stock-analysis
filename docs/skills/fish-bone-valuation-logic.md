---
name: fish-bone-valuation-logic
description: Quantitative logic for 'Fish Head, Body, and Tail' trend analysis for Taiwan stocks.
---

# fish-bone-valuation-logic

## Trigger
When calculating the current trend state or target levels for a specific stock.

## 1. Quantitative Definitions & Logic

### 📉 Dimension A: Fundamental Valuation (The "Value Filter")
Based on the Dynamic Net Value model.
- **UNDERVALUED (低估)**: Price $\le$ Fish Body Baseline ($100\%$).
- **FAIR (合理)**: Fish Body Baseline $< \text{Price} \le \text{Fish Tail Low } (+15\%)$.
- **OVERVALUED (高估)**: Price $>$ Fish Tail Low ($+15\%$).
- **BUBBLE (泡沫)**: Price $\ge$ Fish Bone ($+100\%$).

### 📈 Dimension B: Technical Trend (The "Timing Filter")
- **FISH_HEAD (Trend Initiation)**:
    - **Logic**: Transition from bottom to early uptrend.
    - **Conditions**: Price crosses above $MA_5/MA_{10}$ + MACD Golden Cross.
- **FISH_BODY (Main Trend)**:
    - **Logic**: Established uptrend.
    - **Conditions**: $P > MA_{20} > MA_{60}$ + $ADX > 25$.
- **FISH_TAIL (Late Trend)**:
    - **Logic**: Overextended price action.
    - **Conditions**: $BIAS_{20} > 15-20\%$ + Bearish Divergence.
- **BONE_BROKEN (Exit Signal)**:
    - **Condition**: Price closes below $MA_{20}$ and fails to reclaim.

## 2. Hybrid Investment Matrix (The "Dual-Filter")

| Fundamental \ Technical | FISH_HEAD (Initiation) | FISH_BODY (Main Trend) | FISH_TAIL (Late) | BONE_BROKEN (Exit) |
| :--- | :--- | :--- | :--- | :--- |
| **UNDERVALUED** | 🚀 **STRONG BUY** | ✅ **ADD/HOLD** | ⚠️ **CAUTION** | ❌ **WAIT** |
| **FAIR** | ✅ **BUY** | ✅ **HOLD** | ⚠️ **TAKE PROFIT** | ❌ **EXIT** |
| **OVERVALUED** | ⚠️ **SPECULATIVE** | ⚠️ **TIGHT STOP** | 🚀 **STRONG SELL** | 🚀 **PANIC SELL** |
| **BUBBLE** | ❌ **AVOID** | 🚀 **STRONG SELL** | 🚀 **STRONG SELL** | 🚀 **PANIC SELL** |


## 2. Execution Workflow
1. Fetch data via `tw-stock-api-handler`.
2. Calculate $MA_{20}$, $MA_{60}$, $MACD$, $ADX$, and $BIAS_{20}$.
3. Evaluate conditions in order: `BONE_BROKEN` $\rightarrow$ `FISH_TAIL` $\rightarrow$ `FISH_BODY` $\rightarrow$ `FISH_HEAD`.
4. Output the current state and the value of the "Fish Bone" ($MA_{20}$).

## 3. Verification Standards
- **Input**: Stock Symbol + Timeframe.
- **Output**: `{ "state": "FISH_HEAD|BODY|TAIL|BROKEN", "fish_bone_value": float, "bias": float, "adx": float }`
