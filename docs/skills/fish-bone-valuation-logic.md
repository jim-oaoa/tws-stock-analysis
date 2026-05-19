---
name: fish-bone-valuation-logic
description: Quantitative logic for 'Fish Head, Body, and Tail' trend analysis for Taiwan stocks.
---

# fish-bone-valuation-logic

## Trigger
When calculating the current trend state or target levels for a specific stock.

## 1. Quantitative Definitions & Logic

### 🐟 Stage 1: Fish Head (Trend Initiation)
- **Logic**: Transition from bottom/consolidation to early uptrend.
- **Conditions**:
    1. **MA Breakout**: Price ($P$) crosses above short-term Moving Average (e.g., $MA_5$ or $MA_{10}$).
    2. **MACD Golden Cross**: $DIF$ crosses above the Signal line.
    3. **Context**: Occurrence typically happens below or near the zero axis.
- **State**: `FISH_HEAD` (High risk, low confirmation).

### 🐟 Stage 2: Fish Body & Bone (Main Trend)
- **Logic**: Established uptrend with high probability of profit.
- **Conditions**:
    1. **Bullish Alignment**: $P > MA_{20} > MA_{60}$ and both slopes $\ge 0$.
    2. **Trend Strength**: $ADX > 25$ (Confirming strong directional move, not ranging).
- **The Fish Bone (Defense Line)**:
    - Defined as the $MA_{20}$ (Monthly Line).
    - **Defense Condition**: $P \ge MA_{20}$.
- **State**: `FISH_BODY` (Optimal holding period).

### 🐟 Stage 3: Fish Tail (Late Trend / Blow-off Top)
- **Logic**: Overextended price action with extreme sentiment.
- **Conditions**:
    1. **Excessive Bias (BIAS)**:
        - Large Cap: $BIAS_{20} > 15\%$.
        - Small/Mid Cap: $BIAS_{20} > 20\%$.
    2. **Divergence**: Price makes a new high ($P_{new} > P_{old}$), but RSI or MACD $DIF$ fails to make a new high.
- **State**: `FISH_TAIL` (High risk, profit-taking zone).

### 💀 Bone Break (Exit Signal)
- **Condition**: Price $P$ closes below $MA_{20}$ and fails to reclaim it within 3 trading days.
- **Action**: Immediate Exit / Full Clear.

## 2. Execution Workflow
1. Fetch data via `tw-stock-api-handler`.
2. Calculate $MA_{20}$, $MA_{60}$, $MACD$, $ADX$, and $BIAS_{20}$.
3. Evaluate conditions in order: `BONE_BROKEN` $\rightarrow$ `FISH_TAIL` $\rightarrow$ `FISH_BODY` $\rightarrow$ `FISH_HEAD`.
4. Output the current state and the value of the "Fish Bone" ($MA_{20}$).

## 3. Verification Standards
- **Input**: Stock Symbol + Timeframe.
- **Output**: `{ "state": "FISH_HEAD|BODY|TAIL|BROKEN", "fish_bone_value": float, "bias": float, "adx": float }`
