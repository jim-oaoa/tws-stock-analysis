# TASK_TICKET_001: Production-Grade Valuation Engine & Dashboard

## 📋 Overview
Transition the Proof of Concept (PoC) into a production-grade valuation engine based on the "Fish-Bone" (魚頭魚尾魚骨) model.

## 🛠️ Technical Requirements
### 1. Valuation Logic (Fundamental)
- **Net Value Recursion**: Implement $NetValue_{t} = NetValue_{t-1} + (EPS_t + OCI_t + Other_t + Dividends_t)$.
- **Valuation Zones (Multipliers)**:
    - Fish Head ( undervalued): 0.85x Baseline
    - Fish Body (fair value): 1.00x Baseline
    - Fish Tail Low (slightly overvalued): 1.15x Baseline
    - Fish Tail High (overvalued): 1.30x Baseline
    - Fish Bone (critical support/resistance): 2.00x Baseline

### 2. Hybrid Signal Matrix (Technical + Fundamental)
- **Technical State**: 
    - Trend: Price relative to MA20/MA60.
    - Momentum: MACD Golden Cross/Death Cross.
    - Strength: ADX > 25.
    - Overextension: BIAS20 (e.g., > 15-20% as "Fish Tail" warning).
- **Signal Output**: Intersection of Fundamental Zone and Technical State $\rightarrow$ `STRONG BUY`, `BUY`, `HOLD`, `SELL`, `STRONG SELL`.

### 3. Deliverables
- `src/valuation/models.py`: Data classes for Valuation results and Signal types.
- `src/valuation/engine.py`: Core calculation logic.
- `src/valuation/api.py`: FastAPI endpoint `GET /api/valuation/{symbol}`.

## ✅ Acceptance Criteria (AC)
- [ ] AC0: `NetValue` calculation matches the recursive formula across 5+ years of data.
- [ ] AC1: Valuation zones (Head/Body/Tail/Bone) are correctly computed relative to baseline.
- [ ] AC2: Technical indicators are successfully integrated from the API handler.
- [ ] AC3: The Hybrid Signal Matrix returns correct signals based on the defined matrix.
- [ ] AC4: API endpoint returns a valid JSON response including all zones and the current signal.
- [ ] AC5: All code passes Ruff (linting) and Mypy (typing).

## 📅 Status
- Status: IN_PROGRESS
- Assignee: Hermes (Orchestrator) / Cursor (Maker)
