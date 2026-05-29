"""FastAPI 應用：GET /api/valuation/{symbol}"""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from src.db.repository import StockRepository
from src.db.schema import get_session_factory
from src.scoring.engine import HealthCheckEngine
from src.scoring.models import HealthCheckResult
from src.services.hybrid_signal import HybridSignalService
from src.valuation.models import HybridSignalResult, ValuationApiResponse

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEB_DIR = PROJECT_ROOT / "web"

app = FastAPI(title="TWS Stock Valuation API")


@app.get("/health")
def health():
    return {"status": "ok", "app": "TWS Stock Valuation API"}
SessionLocal = get_session_factory()

if WEB_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


def _get_repo() -> StockRepository:
    session: Session = SessionLocal()
    return StockRepository(session)


@app.get("/api/valuation/{symbol}", response_model=ValuationApiResponse)
def get_valuation(symbol: str) -> ValuationApiResponse:
    repo = _get_repo()
    try:
        sym = symbol.upper()
        initial = repo.get_initial_net_value(sym)
        price = repo.get_current_price(sym)
        financials = repo.get_financials(sym)
        return HybridSignalService.get_valuation(sym, price, financials, initial)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        repo._session.close()


@app.get("/api/signal/{symbol}", response_model=HybridSignalResult)
def get_hybrid_signal(symbol: str) -> HybridSignalResult:
    repo = _get_repo()
    try:
        sym = symbol.upper()
        initial = repo.get_initial_net_value(sym)
        price = repo.get_current_price(sym)
        financials = repo.get_financials(sym)
        bars = repo.get_price_bars_df(sym)
        return HybridSignalService.get_hybrid_signal(
            sym, price, financials, initial, bars
        )
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    finally:
        repo._session.close()


def _load_stocks() -> list[dict]:
    """從 twse_stocks.json 載入股票清單"""
    stocks_path = PROJECT_ROOT / "src" / "data" / "twse_stocks.json"
    if not stocks_path.is_file():
        return []
    with open(stocks_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/stocks/search")
def search_stocks(q: str = Query(default="", description="股票代碼或名稱關鍵字")):
    """搜尋股票（代碼或名稱部分匹配，不分大小寫）"""
    if not q:
        return []
    query = q.lower().strip()
    stocks = _load_stocks()
    results = []
    for stock in stocks:
        if query in stock["code"].lower() or query in stock["name"].lower():
            results.append(stock)
    return results[:10]


@app.get("/api/health-check/{symbol}", response_model=HealthCheckResult)
def health_check(symbol: str) -> HealthCheckResult:
    """一鍵健檢評分"""
    repo = _get_repo()
    try:
        sym = symbol.upper()
        df = repo.get_price_bars_df(sym)
        result = HealthCheckEngine.evaluate(df, stock_name=sym)
        return result
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    finally:
        repo._session.close()


@app.get("/")
def valuation_ui():
    index = WEB_DIR / "valuation.html"
    if not index.is_file():
        raise HTTPException(status_code=404, detail="valuation.html not found")
    return FileResponse(index)
