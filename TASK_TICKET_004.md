# TASK_TICKET_004: Reconcile Dual Codebase — Models, Engine, and Service Layer

## Overview

The codebase has **two divergent implementations** that must be reconciled. The `src/valuation/engine.py` + `src/valuation/models.py` represent one API (function-based, limited enums). The `src/services/hybrid_signal.py` + `src/technical/analysis.py` + `tests/test_truth_table.py` represent another API (class-based with ValuationEngine, richer enums). These two halves cannot import each other, causing 4/7 tests to fail at collection and `hybrid_signal.py` to be completely non-functional.

## Root Cause Map

| File | Problem | Detail |
|------|---------|--------|
| `src/valuation/models.py` | Missing enums | `TechnicalState` lacks FISH_BODY, FISH_TAIL, BONE_BROKEN; no `FinalSignal` enum |
| `src/valuation/engine.py` | Missing class + wrong states | No `ValuationEngine` class; `classify_technical_state` returns BULLISH/BEARISH but should return FISH_BODY/FISH_TAIL/BONE_BROKEN |
| `src/services/hybrid_signal.py` | Import errors | `ValuationEngine`, `FinalSignal`, `TechnicalState.FISH_BODY` don't exist; `ValuationZone` enum imported but models has `ValuationZoneLevels` |
| `tests/test_truth_table.py` | Import errors | Direct import of `ValuationEngine`, `FinalSignal` |
| `tests/test_engine.py` | Float precision | Line 23: `assertEqual(3.1500000000000004, 3.15)` |

## Technical Requirements

### 1. Update `src/valuation/models.py`

Add missing enum members to **TechnicalState**:
```python
class TechnicalState(str, Enum):
    FISH_HEAD = "FISH_HEAD"
    FISH_BODY = "FISH_BODY"       # NEW
    FISH_TAIL = "FISH_TAIL"       # NEW
    BONE_BROKEN = "BONE_BROKEN"   # NEW
    BULLISH = "BULLISH"
    NEUTRAL = "NEUTRAL"
    BEARISH = "BEARISH"
    OVEREXTENDED = "OVEREXTENDED"
```

Add **FinalSignal** enum:
```python
class FinalSignal(str, Enum):
    STRONG_BUY = "STRONG_BUY"
    ADD_HOLD = "ADD_HOLD"
    BUY = "BUY"
    HOLD = "HOLD"
    TIGHT_STOP = "TIGHT_STOP"
    STRONG_SELL = "STRONG_SELL"
    EXIT = "EXIT"
```

### 2. Update `src/valuation/engine.py`

**2a.** Update `classify_technical_state` logic to return FISH_BODY/FISH_TAIL/BONE_BROKEN (align with `src/technical/analysis.py` evaluate() method). Reference: technical/analysis.py lines 88-110 for the correct state precedence.

**2b.** Add a `ValuationEngine` class that wraps existing standalone functions. Required static methods:

```python
class ValuationEngine:
    @staticmethod
    def calculate_valuation_zones(net_value: float) -> ValuationZoneLevels:
        return compute_zones(net_value)

    @staticmethod
    def calculate_accumulated_net_values(records, initial_net_value=0.0):
        grid = compute_net_value(records, initial_net_value)
        return [cell.accumulated_net_value for cell in grid]

    @staticmethod
    def get_full_valuation_state(symbol, price, financials, initial_net_value=0.0):
        sorted_fin = sorted(financials, key=lambda x: (x.year, x.quarter))
        grid = compute_net_value(sorted_fin, initial_net_value)
        net_value = grid[-1].accumulated_net_value if grid else initial_net_value
        zones = compute_zones(net_value)
        _, current_zone = determine_fundamental_zone(price, zones)
        return ValuationResult(
            symbol=symbol,
            price=price,
            net_value=net_value,
            zones=zones,
            current_zone=current_zone,
        )
```

### 3. Fix `src/services/hybrid_signal.py`

- Replace `from src.valuation.engine import ValuationEngine` -> `from src.valuation.engine import ValuationEngine, compute_zones`
- Replace `FinalSignal` imports -> remove (now in models, already imported)
- Fix `ValuationZone` type mismatch: `determine_fundamental_zone(price, zones: ValuationZoneLevels)` should use `ValuationZoneLevels` from models
- The truth table `_TRUTH_TABLE` references `FinalSignal` and `TechnicalState` — ensure after models update these resolve correctly

### 4. Fix `tests/test_truth_table.py`

- Replace `from src.valuation.engine import ValuationEngine` -> `from src.valuation.engine import ValuationEngine` (should resolve after fix #2b)
- Replace `FinalSignal` import — remove, already in models via hybrid_signal imports
- Fix fixture: `ValuationEngine.calculate_valuation_zones(26.30)` — ensure this works after fix #2b

### 5. Fix `tests/test_engine.py` line 23

```python
# Before:
self.assertEqual(grid[1].accumulated_net_value, 3.15)
# After:
self.assertAlmostEqual(grid[1].accumulated_net_value, 3.15, places=10)
```

## Verification (Acceptance Criteria)

- [ ] AC0: `python3 -c "from src.valuation.models import TechnicalState; print(TechnicalState.FISH_BODY)"` succeeds
- [ ] AC1: `python3 -c "from src.valuation.engine import ValuationEngine; print(ValuationEngine.calculate_valuation_zones(100.0))"` succeeds
- [ ] AC2: `python3 -c "from src.services.hybrid_signal import HybridSignalService"` succeeds
- [ ] AC3: `python3 -m pytest tests/test_engine.py -v` — all 3 pass
- [ ] AC4: `python3 -m pytest tests/test_truth_table.py -v` — all 4 pass
- [ ] AC5: `python3 -m pytest tests/ -v` — 7/7 pass, 0 failures, 0 errors
- [ ] AC6: `python3 -c "from src.main import app"` — no import errors

## Status

- Status: COMPLETED
- Assignee: Subagent (Maker)
- Auditor: Hermes (Orchestrator)
- Completed: 2026-05-25 | 17/17 tests pass
