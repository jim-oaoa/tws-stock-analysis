---
name: tw-stock-api-handler
description: SOP for acquiring and standardizing Taiwan stock market data.
---

# tw-stock-api-handler

## Trigger
When the system needs to fetch K-line data, dividend information, or real-time quotes for Taiwan stocks.

## 1. Recommended Data Sources (Priority)
- **Primary**: `yfinance` (Yahoo Finance) - Best for rapid prototyping and historical data.
- **Secondary**: `FinMind` - Best for precise financial indicators and adjusted dividend data.
- **Tertiary**: TWSE (Taiwan Stock Exchange) Official API - Used for final verification.

## 2. Standardization Workflow
- **Date Format**: All dates must be in `ISO 8601` (`YYYY-MM-DD`).
- **Price Adjustment**: Historical K-lines must be explicitly labeled as `Adjusted Close` to avoid gap errors caused by dividends/splits.
- **Missing Value Handling**:
    - Use `Forward Fill` for non-trading days.
    - Log all filling events in the system log.

## 3. Pitfalls & Mitigation
- **Rate Limiting**: Implement `exponential backoff`. Interval between requests $\ge 1$ second.
- **Timeouts**: Set a 10s timeout. If failed, automatically failover to the secondary source.
- **Data Drift**: Always verify the most recent 3 days of data against the official TWSE website if a drastic move is detected.

## 4. Verification Standards
- **Output Format**: Must return a `Pandas DataFrame` or a standardized `JSON` array.
- **Required Columns**: `Date`, `Open`, `High`, `Low`, `Close`, `Volume`.
- **Integrity Check**: No `NaN` values in the final output.
