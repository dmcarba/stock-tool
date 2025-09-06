from abc import ABC, abstractmethod
from typing import List
from ..models.models import Ticker

class PortfolioRepository(ABC):
    
    @abstractmethod
    def save_tracked_tickers(self, tickers: List[Ticker]):
        pass
    
    @abstractmethod
    def get_tracked_tickers(self) -> List[Ticker]:
        pass
    
    @abstractmethod
    def get_tracked_ticker_by_symbol(self, symbol: str) -> Ticker:
        pass
    
    @abstractmethod
    def delete_tracked_ticker_by_symbol(self, symbol: str):
        pass
    