import time
import logging
from typing import List, Tuple, Optional
from datetime import datetime
import yfinance as yf
import pandas as pd

from .models import FinancialQuarterly

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockRepository:
    """
    Production-grade repository for fetching Taiwan stock data using yfinance.
    Supports financial statement extraction and historical price series.
    """

    def __init__(self, rate_limit_interval: float = 1.0):
        self.rate_limit_interval = rate_limit_interval
        self._last_request_time = 0.0

    def _apply_rate_limit(self):
        """Ensures requests are spaced by the configured interval."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit_interval:
            time.sleep(self.rate_limit_interval - elapsed)
        self._last_request_time = time.time()

    def _get_quarter(self, date: datetime) -> int:
        """Calculates the calendar quarter (1-4) from a date."""
        return (date.month - 1) // 3 + 1

    def get_financials(self, symbol: str) -> List[FinancialQuarterly]:
        """
        Fetches quarterly income statements and balance sheets to map to FinancialQuarterly models.
        
        Args:
            symbol: Stock symbol (e.g., '2330.TW' for TSMC).
            
        Returns:
            A list of FinancialQuarterly objects sorted by date descending.
        """
        self._apply_rate_limit()
        
        try:
            ticker = yf.Ticker(symbol)
            
            # Fetch quarterly data
            q_financials = ticker.quarterly_financials
            q_cashflow = ticker.quarterly_cashflow
            
            if q_financials.empty:
                logger.warning(f"No quarterly financials found for {symbol}. Returning empty list.")
                return []

            # We iterate over the columns (dates)
            financials_list = []
            dates = q_financials.columns

            for date in dates:
                # Handle pandas Timestamp
                dt = date.to_pydatetime() if hasattr(date, 'to_pydatetime') else date
                year = dt.year
                quarter = self._get_quarter(dt)
                
                # 1. Extract EPS
                eps = 0.0
                for label in ["Basic EPS", "Diluted EPS"]:
                    if label in q_financials.index:
                        val = q_financials.loc[label, date]
                        if pd.notnull(val):
                            eps = float(val)
                            break
                
                # Fallback: Calculate EPS from Net Income / Shares Outstanding if possible
                if eps == 0.0 and "Net Income" in q_financials.index:
                    net_income = q_financials.loc["Net Income", date]
                    shares = ticker.info.get('sharesOutstanding')
                    if pd.notnull(net_income) and shares:
                        eps = float(net_income) / shares

                # 2. Extract Dividends (Quarterly Cash flow)
                dividends = 0.0
                if not q_cashflow.empty:
                    for label in ["Cash Dividends Paid", "Dividends Paid"]:
                        if label in q_cashflow.index:
                            val = q_cashflow.loc[label, date]
                            if pd.notnull(val):
                                dividends = abs(float(val))
                                break

                # 3. OCI, Other Items, Adjustment Amount
                oci = 0.0
                other_items = 0.0
                adjustment_amount = 0.0

                for label in q_financials.index:
                    lbl_upper = label.upper()
                    if "COMPREHENSIVE INCOME" in lbl_upper and "NET" not in lbl_upper:
                        val = q_financials.loc[label, date]
                        if pd.notnull(val):
                            oci = float(val)
                    elif "ADJUSTMENT" in lbl_upper:
                        val = q_financials.loc[label, date]
                        if pd.notnull(val):
                            adjustment_amount = float(val)

                if eps == 0.0:
                    logger.warning(f"Missing EPS for {symbol} in {year} Q{quarter}. Defaulting to 0.0")

                financials_list.append(FinancialQuarterly(
                    symbol=symbol,
                    year=year,
                    quarter=quarter,
                    eps=eps,
                    oci=oci,
                    other_items=other_items,
                    dividends=dividends,
                    adjustment_amount=adjustment_amount
                ))

            return financials_list

        except Exception as e:
            logger.error(f"Error fetching financials for {symbol}: {e}")
            return []

    def get_price_series(self, symbol: str, period: str = '1y') -> Tuple[List[float], List[float], List[float]]:
        """
        Fetches adjusted historical price data.
        
        Args:
            symbol: Stock symbol (e.g., '2330.TW').
            period: Period of data to fetch (e.g., '1y', '5y', 'max').
            
        Returns:
            A tuple of three lists: (Highs, Lows, Closes).
        """
        self._apply_rate_limit()
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, auto_adjust=True)
            
            if hist.empty:
                logger.error(f"No price data found for symbol {symbol}.")
                return [], [], []
            
            highs = hist['High'].tolist()
            lows = hist['Low'].tolist()
            closes = hist['Close'].tolist()
            
            return highs, lows, closes
            
        except Exception as e:
            logger.error(f"Error fetching price series for {symbol}: {e}")
            return [], [], []
