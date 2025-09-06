"""SQLite portfolio repository implementation."""

import sqlite3
from typing import List
from .portfolio_repository import PortfolioRepository
from ..models.models import Ticker

class SQLitePortfolioRepository(PortfolioRepository):
    """SQLite implementation of portfolio repository."""
    
    def __init__(self, db_path: str = "portfolio.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tickers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT UNIQUE NOT NULL,
                    quantity REAL NOT NULL DEFAULT 0,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def save_tracked_tickers(self, tickers: List[Ticker]):
        """Save tracked tickers to database."""
        with sqlite3.connect(self.db_path) as conn:
            for ticker in tickers:
                conn.execute(
                    """INSERT INTO tickers (symbol, quantity) VALUES (?, ?)
                       ON CONFLICT(symbol) DO UPDATE SET 
                       quantity = excluded.quantity,
                       updated_at = CURRENT_TIMESTAMP""",
                    (ticker.symbol, ticker.quantity)
                )
    
    def get_tracked_tickers(self) -> List[Ticker]:
        """Get all tracked tickers."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tickers")
            return [Ticker(**dict(row)) for row in cursor.fetchall()]
    
    def get_tracked_ticker_by_symbol(self, symbol: str) -> Ticker:
        """Get tracked ticker by symbol."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tickers WHERE symbol = ?", (symbol,))
            row = cursor.fetchone()
            if row:
                return Ticker(**dict(row))
            raise ValueError(f"Ticker {symbol} not found")
    
    def delete_tracked_ticker_by_symbol(self, symbol: str) -> bool:
        """Delete tracked ticker by symbol."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM tickers WHERE symbol = ?", (symbol,))
            if cursor.rowcount == 0:
                raise ValueError(f"Ticker {symbol} not found")
            return True