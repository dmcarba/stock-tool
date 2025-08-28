"""FastAPI application for stock data extraction."""

from fastapi import FastAPI
from .routers.stock_extraction_router import router as stock_router

app = FastAPI(title="Stock Tool API", description="Stock data extraction API")

app.include_router(stock_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)