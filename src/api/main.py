"""FastAPI 應用：GET /api/valuation/{symbol}"""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from src.db.repository import StockRepository
from src.db.schema import get_session_factory
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


@app.get("/")
def valuation_ui():
    index = WEB_DIR / "valuation.html"
    if not index.is_file():
        raise HTTPException(status_code=404, detail="valuation.html not found")
    return FileResponse(index)
