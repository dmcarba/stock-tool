"""Repository factory for creating repository instances."""

import os
from .portfolio_repository import PortfolioRepository
from .sqlite_portfolio_repository import SQLitePortfolioRepository


class RepositoryFactory:
    """Factory for creating repository instances."""
    
    @staticmethod
    def create_portfolio_repository() -> PortfolioRepository:
        """Create portfolio repository based on configuration."""
        repo_type = os.environ.get("PORTFOLIO_REPO_TYPE", "sqlite")
        
        if repo_type == "sqlite":
            db_path = os.environ.get("PORTFOLIO_DB_PATH", "portfolio.db")
            return SQLitePortfolioRepository(db_path)
        
        raise ValueError(f"Unknown repository type: {repo_type}")