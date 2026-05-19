---
name: realtime-indicator-dashboard
description: UI/UX standards and performance requirements for the Taiwan Stock Analysis dashboard.
---

# realtime-indicator-dashboard

## Trigger
When designing, developing, or modifying frontend UI components, or configuring data update frequencies.

## 1. Recommended Tech Stack
- **Framework**: `Next.js` (App Router) -> Ensures SEO and fast initial load.
- **Styling**: `Tailwind CSS` -> Fast responsive layout implementation.
- **State Management**: `Zustand` or `React Context` -> Manage selected stock symbols and global state.
- **Real-time**: `WebSocket` or `SSE (Server-Sent Events)` -> Real-time push for quotes and indicator changes.
- **Visualization**: `Lightweight Charts` (TradingView) or `ECharts` -> Plot K-lines and Fish-Bone lines.

## 2. Visual Presentation Standards
- **Fish-Bone Visualization**: 
    - Overlay a dynamic $MA_{20}$ curve directly on the K-line chart.
    - Color: "Fish Bone Yellow" (e.g., `#FFFF00`).
- **Trend State Indicator**:
    - **FISH_HEAD**: Label as `Light Green` -> Tip: "Potential Start, Beware of Fish-Thorns".
    - **FISH_BODY**: Label as `Deep Green` -> Tip: "Main Trend, Hold with Confidence".
    - **FISH_TAIL**: Label as `Bright Red` -> Tip: "Overextended, Prepare to Exit".
    - **BONE_BROKEN**: Label as `Black/Dark Grey` -> Tip: "Bone Broken, Immediate Exit".
- **Indicator Dashboard**:
    - Traffic Light Design: $\text{ADX} > 25$ (Green) / $\text{ADX} < 25$ (Red).
    - BIAS (Deviation) using progress bars, changing color when exceeding thresholds.

## 3. Performance & Update Requirements
- **Update Frequency**: 
    - Quotes -> Every 1-3 seconds.
    - Trend State (Head/Body/Tail) -> Update once per K-line close.
- **Rendering Optimization**: Use `Memoization` (React.memo) to prevent unnecessary full-page re-renders.

## 4. Verification Standards
- **Functional Verification**: Backend state change -> Frontend label color changes immediately -> No noticeable lag.
- **UX Verification**: Fish-bone lines and state labels are clearly visible on both Mobile and PC.
