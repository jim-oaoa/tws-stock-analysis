# TASK_TICKET_003: Fish-Bone Valuation Dashboard

## 📋 Overview
Build a professional web-based dashboard to visualize the results of the Fish-Bone valuation engine. The goal is to provide a clear visual comparison between the current market price and the fundamental valuation zones.

## 🛠️ Technical Stack
- **Framework**: React + Vite
- **Styling**: Tailwind CSS (Dark Mode)
- **Charting**: Lightweight Charts (by TradingView)
- **API**: Integration with `src/valuation/api.py`

## 🎨 Visual Components
### 1. Valuation Price Chart
- **Base**: Candlestick or Line chart of historical prices.
- **Overlays**: 5 horizontal lines representing the valuation zones:
    - Fish Head (0.85x) $\rightarrow$ Green
    - Fish Body (1.00x) $\rightarrow$ Yellow
    - Fish Tail Low (1.15x) $\rightarrow$ Orange
    - Fish Tail High (1.30x) $\rightarrow$ Red-Orange
    - Fish Bone (2.00x) $\rightarrow$ Deep Red
- **Current Price Marker**: A dynamic label showing the current price and its associated zone.

### 2. Net Value Trend Chart
- **X-Axis**: Quarters/Years.
- **Y-Axis**: `accumulated_net_value`.
- **Visual**: A growth curve showing the expansion of the company's intrinsic value.

### 3. Signal Indicator Card
- **Prominent Display**: Current `HybridSignal` (e.g., STRONG BUY).
- **Context**: The `action` description provided by the engine.

### 4. Recursion Grid Table
- **Data**: Display the `QuarterlyGridCell` list.
- **Columns**: Year, Quarter, EPS, OCI, Dividends, Accumulated Net Value.

## ✅ Acceptance Criteria (AC)
- [ ] AC0: Successfully connect to `/valuation/{symbol}` and `/valuation/signal/{symbol}`.
- [ ] AC1: Correct rendering of the 5 valuation horizontal lines on the price chart.
- [ ] AC2: Implementation of symbol switching with full state refresh.
- [ ] AC3: Professional financial-grade UI with Dark Mode.
- [ ] AC4: Responsive layout for desktop and tablet.

## 📅 Status
- Status: IN_PROGRESS
- Assignee: Hermes (Orchestrator) / Frontend Maker
