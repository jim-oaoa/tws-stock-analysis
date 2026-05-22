from fastapi import FastAPI
from src.valuation.api import router as valuation_router

app = FastAPI(
    title="TWS Stock Analysis API",
    description="Fish-Bone Valuation Engine API",
    version="1.0.0"
)

# Include the valuation router
app.include_router(valuation_router)

@app.get("/")
async def root():
    return {"message": "TWS Stock Analysis API is running. Use /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
