"""FastAPI server module."""

import os
import uvicorn
from fastapi import FastAPI
from .routers.stock_extraction_router import router as stock_router

api_port = int(os.environ.get("API_PORT", 8001))
app = FastAPI(title="Stock Tool API", description="Stock data extraction API")
app.include_router(stock_router)

def start_api_server():
    """Start the FastAPI server."""
    print(f"Starting FastAPI server on port {api_port}...")
    uvicorn.run(app, host="0.0.0.0", port=api_port)