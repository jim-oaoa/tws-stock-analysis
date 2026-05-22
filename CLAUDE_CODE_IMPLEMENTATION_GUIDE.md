# 🛠️ MANDATORY IMPLEMENTATION SPECIFICATION (No Guesswork)

## 📌 1. PROJECT ROOT & ARCHITECTURE
**Project Root**: `/mnt/d/AI/hermes/Projects/tws-stock-analysis`

### 📂 Mandatory File Map
| Component | Absolute Path | Status | Requirement |
| :--- | :--- | :--- | :--- |
| **Data Models** | `/mnt/d/AI/hermes/Projects/tws-stock-analysis/src/valuation/models.py` | ✅ Built | MUST use for all type hints |
| **Calculation Engine** | `/mnt/d/AI/hermes/Projects/tws-stock-analysis/src/valuation/engine.py` | ✅ Built | MUST use for all net-value logic |
| **Strategy Skill** | `/mnt/d/AI/hermes/Projects/tws-stock-analysis/docs/skills/fish-bone-valuation-logic.md` | ✅ Built | MUST use as the source of truth for signals |
| **Implementation Guide** | `/mnt/d/AI/hermes/Projects/tws-stock-analysis/CURSOR_IMPLEMENTATION_GUIDE.md` | ✅ Current | The master instruction file |

---

## 🧮 2. ABSOLUTE MATHEMATICAL LOGIC (Do Not Alter)

### A. Net Value Accumulation Formula
The calculation MUST follow this recursive formula:
$$\text{NetValue}_{t} = \text{NetValue}_{t-1} + (\text{EPS}_t + \text{OCI}_t + \text{Other}_t + \text{Dividends}_t)$$
**CRITICAL**: $\text{Dividends}$ are provided as **negative numbers** (e.g., -1.49). Therefore, you MUST use **addition** (`+ dividends`), NOT subtraction.

### B. Baseline Definition
$$\text{Baseline (Adjusted Net Value)} = \text{Latest Accumulated Net Value} + \text{Adjustment Amount}$$

### C. Valuation Zone Constants (Fixed Multipliers)
These values are absolute. Do not change them:
- **Fish Head (魚頭)**: $\text{Baseline} \times 0.85$ (Fixed -15%)
- **Fish Body (魚身)**: $\text{Baseline} \times 1.00$ (Fixed 0%)
- **Fish Tail Low (魚尾低)**: $\text{Baseline} \times 1.15$ (Fixed +15%)
- **Fish Tail High (魚尾高)**: $\text{Baseline} \times 1.30$ (Fixed +30%)
- **Fish Bone (魚骨)**: $\text{Baseline} \times 2.00$ (Fixed +100%)

---

## 🚦 3. HYBRID SIGNAL LOGIC (Truth Table)

The final signal MUST be determined by the intersection of **Fundamental Zone** and **Technical State**.

| Fundamental Zone | Technical State | FINAL SIGNAL | Action |
| :--- | :--- | :--- | :--- |
| `UNDERVALUED` ($\le$ Body) | `FISH_HEAD` | 🚀 **STRONG BUY** | Immediate Entry |
| `UNDERVALUED` ($\le$ Body) | `FISH_BODY` | ✅ **ADD/HOLD** | Accumulate |
| `FAIR` (Body $\to$ Tail Low) | `FISH_HEAD` | ✅ **BUY** | Strategic Entry |
| `FAIR` (Body $\to$ Tail Low) | `FISH_BODY` | ✅ **HOLD** | Maintain Position |
| `OVERVALUED` ($>$ Tail Low) | `FISH_BODY` | ⚠️ **TIGHT STOP** | Raise Stop-loss |
| `OVERVALUED` ($>$ Tail Low) | `FISH_TAIL` | 🚀 **STRONG SELL** | Take Profit |
| `BUBBLE` ($\ge$ Bone) | ANY STATE | 🚀 **STRONG SELL** | Full Exit |
| ANY ZONE | `BONE_BROKEN` | ❌ **EXIT** | Immediate Stop-out |

---

## 🛠️ 4. MANDATORY IMPLEMENTATION STEPS

### Step 1: Database Integration
- **Required Field**: Add `initial_net_value` (float) to the stock metadata table. This is the starting seed for the accumulation formula.
- **Financials Table**: Create/Use a table that stores `year`, `quarter`, `eps`, `oci`, `other_items`, `dividends`, and `adjustment_amount`.

### Step 2: API Development
- **Endpoint**: `GET /api/valuation/{symbol}`
- **Logic**: 
    1. Fetch `initial_net_value` $\rightarrow$ 2. Fetch all `FinancialQuarterly` records $\rightarrow$ 3. Pass to `ValuationEngine` $\rightarrow$ 4. Return `StockValuationState`.

### Step 3: Hybrid Signal Service
- Implement a service that calls both the `ValuationEngine` and the `TechnicalAnalysis` module.
- Apply the **Truth Table** from Section 3 to return the `FINAL SIGNAL`.

### Step 4: UI Specification
- **View**: A grid table with quarters on X-axis and valuation metrics on Y-axis.
- **Visuals**: 
    - Background Green if Price $\le$ Baseline.
    - Background Red if Price $\ge$ Fish Bone.

---

## ⚠️ FINAL WARNINGS FOR CURSOR
1. **NO GUESSING**: If a value is not in the DB, return a 404 or Error; do not assume defaults.
2. **PATH STRICTNESS**: Use the absolute paths defined in Section 1.
3. **TYPE SAFETY**: Use the Pydantic models in `models.py` for all data transfers.
