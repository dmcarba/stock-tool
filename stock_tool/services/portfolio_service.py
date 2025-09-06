"""Portfolio service for managing tracked tickers."""

from typing import List
from ..repositories.repository_factory import RepositoryFactory
from ..models.models import Ticker


class PortfolioService:
    """Service for portfolio management operations."""
    
    def __init__(self) -> None:
        self.repository = RepositoryFactory.create_portfolio_repository()
    
    def get_all_tracked_tickers(self) -> List[Ticker]:
        """Get all tracked tickers."""
        return self.repository.get_tracked_tickers()
    
    def get_tracked_ticker(self, symbol: str) -> Ticker:
        """Get tracked ticker by symbol."""
        return self.repository.get_tracked_ticker_by_symbol(symbol)
    
    def add_ticker(self, symbol: str, quantity: float):
        """Add ticker to portfolio."""
        ticker = Ticker(symbol=symbol, quantity=quantity)
        self.repository.save_tracked_tickers([ticker])
    
    def remove_ticker(self, symbol: str):
        """Remove ticker from portfolio."""
        self.repository.delete_tracked_ticker_by_symbol(symbol)
    
