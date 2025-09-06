"""FastAPI server module."""

import os
import uvicorn
from fastapi import FastAPI
from .routers.stock_extraction_router import router as stock_router
from .routers.portfolio_router import router as portfolio_router
from .routers.index_listing_router import router as index_router

api_port = int(os.environ.get("API_PORT", 8001))
app = FastAPI(title="Stock Tool API", description="Stock data extraction API")
app.include_router(stock_router)
app.include_router(portfolio_router)
app.include_router(index_router)

def start_api_server():
    """Start the FastAPI server."""
    print(f"Starting FastAPI server on port {api_port}...")
    uvicorn.run(app, host="0.0.0.0", port=api_port)