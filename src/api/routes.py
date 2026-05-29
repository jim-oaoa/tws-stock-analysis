"""API 路由：股票搜尋 + 健檢評分"""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, Query
from src.db.repository import StockRepository
from src.db.schema import get_session_factory
from src.scoring.engine import HealthCheckEngine
from src.scoring.models import HealthCheckResult
from sqlalchemy.orm import Session

PROJECT_ROOT = Path(__file__).resolve().parents[2]

router = APIRouter(prefix="/api", tags=["search", "health-check"])
SessionLocal = get_session_factory()

def _get_repo() -> StockRepository:
    session: Session = SessionLocal()
    return StockRepository(session)

def _load_stocks() -> list[dict]:
    stocks_path = PROJECT_ROOT / "src" / "data" / "twse_stocks.json"
    if not stocks_path.is_file():
        return []
    with open(stocks_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/stocks/search")
def search_stocks(q: str = Query(default="", description="股票代碼或名稱關鍵字")):
    if not q:
        return []
    query = q.lower().strip()
    stocks = _load_stocks()
    results = [s for s in stocks if query in s["code"].lower() or query in s["name"].lower()]
    return results[:10]

@router.get("/health-check/{symbol}", response_model=HealthCheckResult)
def health_check(symbol: str) -> HealthCheckResult:
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
