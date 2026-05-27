from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.valuation.api import router as valuation_router

app = FastAPI(
    title="TWS Stock Analysis API",
    description="Fish-Bone Valuation Engine API",
    version="1.0.0"
)

# CORS — allow frontend dev server (localhost:5174) to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the valuation router
app.include_router(valuation_router)

@app.get("/")
async def root():
    return {"message": "TWS Stock Analysis API is running. Use /docs for API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
