"""資料存取層：缺資料時拋出 LookupError（不猜測預設值）。"""

from typing import List

import pandas as pd
from sqlalchemy.orm import Session

from src.db.schema import FinancialQuarterlyRow, PriceBarRow, StockMetadata
from src.valuation.models import FinancialQuarterly


class StockRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_stock_or_raise(self, symbol: str) -> StockMetadata:
        row = self._session.get(StockMetadata, symbol.upper())
        if row is None:
            raise LookupError(f"Stock metadata not found: {symbol}")
        return row

    def get_initial_net_value(self, symbol: str) -> float:
        return self.get_stock_or_raise(symbol).initial_net_value

    def get_current_price(self, symbol: str) -> float:
        return self.get_stock_or_raise(symbol).current_price

    def get_financials(self, symbol: str) -> List[FinancialQuarterly]:
        stock = self.get_stock_or_raise(symbol)
        rows = (
            self._session.query(FinancialQuarterlyRow)
            .filter(FinancialQuarterlyRow.symbol == stock.symbol)
            .order_by(FinancialQuarterlyRow.year, FinancialQuarterlyRow.quarter)
            .all()
        )
        if not rows:
            raise LookupError(f"No financial quarterly data for: {symbol}")
        return [
            FinancialQuarterly(
                symbol=r.symbol,
                year=r.year,
                quarter=r.quarter,
                eps=r.eps,
                oci=r.oci,
                other_items=r.other_items,
                dividends=r.dividends,
                adjustment_amount=r.adjustment_amount,
            )
            for r in rows
        ]

    def get_price_bars_df(self, symbol: str) -> pd.DataFrame:
        stock = self.get_stock_or_raise(symbol)
        rows = (
            self._session.query(PriceBarRow)
            .filter(PriceBarRow.symbol == stock.symbol)
            .order_by(PriceBarRow.bar_date)
            .all()
        )
        if not rows:
            raise LookupError(f"No price bar data for: {symbol}")
        return pd.DataFrame(
            {
                "Date": [r.bar_date.isoformat() for r in rows],
                "Open": [r.open for r in rows],
                "High": [r.high for r in rows],
                "Low": [r.low for r in rows],
                "Close": [r.close for r in rows],
                "Volume": [r.volume for r in rows],
            }
        )
