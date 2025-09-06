"""Portfolio router for managing tracked tickers."""

from fastapi import APIRouter, HTTPException
from typing import List
from ..services.portfolio_service import PortfolioService
from ..models.models import Ticker

class PortfolioRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/portfolio", tags=["portfolio"])
        self.service = PortfolioService()
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.get("/tickers", response_model=List[Ticker])(self.get_tracked_tickers)
        self.router.get("/tickers/{symbol}", response_model=Ticker)(self.get_tracked_ticker)
        self.router.post("/tickers")(self.save_tracked_tickers)
        self.router.delete("/tickers/{symbol}")(self.delete_tracked_ticker)
    
    def get_tracked_tickers(self):
        """Get all tracked tickers."""
        return self.service.get_all_tracked_tickers()
    
    def get_tracked_ticker(self, symbol: str):
        """Get tracked ticker by symbol."""
        try:
            return self.service.get_tracked_ticker(symbol)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    def save_tracked_tickers(self, tickers: List[Ticker]):
        """Save tracked tickers."""
        try:
            return self.service.repository.save_tracked_tickers(tickers)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save tickers: {str(e)}")
    
    def delete_tracked_ticker(self, symbol: str):
        """Delete tracked ticker by symbol."""
        try:
            return self.service.remove_ticker(symbol)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete ticker: {str(e)}")

router = PortfolioRouter().router
