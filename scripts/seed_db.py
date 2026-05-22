"""初始化 SQLite 並寫入測試資料（對應 test_valuation.py 範例）。"""

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.db.schema import (
    Base,
    FinancialQuarterlyRow,
    PriceBarRow,
    StockMetadata,
    get_engine,
    get_session_factory,
)


def seed():
    engine = get_engine()
    Base.metadata.create_all(engine)
    session = get_session_factory()()

    symbol = "TEST"
    session.query(PriceBarRow).filter(PriceBarRow.symbol == symbol).delete()
    session.query(FinancialQuarterlyRow).filter(
        FinancialQuarterlyRow.symbol == symbol
    ).delete()
    session.query(StockMetadata).filter(StockMetadata.symbol == symbol).delete()

    session.add(
        StockMetadata(symbol=symbol, initial_net_value=24.47, current_price=25.0)
    )
    quarters = [
        (2019, 1, 0.35, 0.22, 0.64, 0.00, 0.0),
        (2019, 2, 0.44, 0.19, -0.10, -1.49, 0.0),
        (2019, 3, 0.61, 0.08, -0.01, 0.00, 0.91),
    ]
    for year, quarter, eps, oci, other_items, dividends, adj in quarters:
        session.add(
            FinancialQuarterlyRow(
                symbol=symbol,
                year=year,
                quarter=quarter,
                eps=eps,
                oci=oci,
                other_items=other_items,
                dividends=dividends,
                adjustment_amount=adj,
            )
        )

    base_date = date(2024, 1, 2)
    price = 22.0
    for i in range(80):
        d = base_date + timedelta(days=i)
        if d.weekday() >= 5:
            continue
        price += 0.08
        session.add(
            PriceBarRow(
                symbol=symbol,
                bar_date=d,
                open=price - 0.2,
                high=price + 0.3,
                low=price - 0.4,
                close=price,
                volume=1000000.0,
            )
        )

    session.commit()
    session.close()
    print("Seed complete: symbol=TEST")


if __name__ == "__main__":
    seed()
