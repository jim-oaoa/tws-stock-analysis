"""SQLAlchemy 資料表定義（路徑依 CURSOR_IMPLEMENTATION_GUIDE）。"""

from datetime import date
from pathlib import Path

from sqlalchemy import Date, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

PROJECT_ROOT = Path("d:/AI/hermes/Projects/tws-stock-analysis")
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DB_URL = f"sqlite:///{DATA_DIR.as_posix()}/tws_stock.db"


class Base(DeclarativeBase):
    pass


class StockMetadata(Base):
    __tablename__ = "stock_metadata"

    symbol: Mapped[str] = mapped_column(String(16), primary_key=True)
    initial_net_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)

    financials: Mapped[list["FinancialQuarterlyRow"]] = relationship(
        back_populates="stock", cascade="all, delete-orphan"
    )
    price_bars: Mapped[list["PriceBarRow"]] = relationship(
        back_populates="stock", cascade="all, delete-orphan"
    )


class FinancialQuarterlyRow(Base):
    __tablename__ = "financial_quarterly"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(
        String(16), ForeignKey("stock_metadata.symbol"), nullable=False
    )
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    quarter: Mapped[int] = mapped_column(Integer, nullable=False)
    eps: Mapped[float] = mapped_column(Float, nullable=False)
    oci: Mapped[float] = mapped_column(Float, default=0.0)
    other_items: Mapped[float] = mapped_column(Float, default=0.0)
    dividends: Mapped[float] = mapped_column(Float, default=0.0)
    adjustment_amount: Mapped[float] = mapped_column(Float, default=0.0)

    stock: Mapped["StockMetadata"] = relationship(back_populates="financials")


class PriceBarRow(Base):
    __tablename__ = "price_bars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(
        String(16), ForeignKey("stock_metadata.symbol"), nullable=False
    )
    bar_date: Mapped[date] = mapped_column(Date, nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)

    stock: Mapped["StockMetadata"] = relationship(back_populates="price_bars")


def get_engine(db_url: str = DEFAULT_DB_URL):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return create_engine(db_url, connect_args={"check_same_thread": False})


def get_session_factory(db_url: str = DEFAULT_DB_URL):
    engine = get_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
