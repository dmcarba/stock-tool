import yfinance as yf
import pandas as pd
import logging
from typing import Dict, List, Any

class StockExtractionService:
    """Service for extracting stock data from Yahoo Finance."""
    
    sectors = [
    "basic materials",
    "communication services",
    "consumer cyclical",
    "consumer defensive",
    "energy",
    "financial services",
    "healthcare",
    "industrials",
    "real estate",
    "technology",
    "utilities"
    ]
    
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
    
    def extract_ticker_info(self, ticker: str) -> Dict[str, Any]:
        """Extract basic ticker information from Yahoo Finance.
        
        Returns company info including symbol, name, market cap, sector, etc.
        """
        self.logger.info(f"Extracting ticker info for {ticker}")
        result = self._getTicker(ticker).info
        if not result or len(result) == 0:
            self.logger.warning(f"No ticker info found for {ticker}")
        return result
        
    def extract_quarterly_financials(self, symbol: str) -> List[Dict[str, Any]]:
        """Extract quarterly financial statements data.
        
        Combines income statement, balance sheet, and cash flow data for quarterly periods.
        """
        self.logger.info(f"Extracting quarterly financials for {symbol}")
        stock = self._getTicker(symbol)
        # Join all three financial statements for comprehensive quarterly data
        df = self._join_financial_statements(
            stock.quarterly_financials.transpose(),
            stock.quarterly_balance_sheet.transpose(),
            stock.quarterly_cash_flow.transpose()
        )
        if df.empty:
            self.logger.warning(f"No quarterly financials found for {symbol}")
        return self._df_to_json_safe(df)
    
    def extract_yearly_financials(self, symbol: str) -> List[Dict[str, Any]]:
        """Extract annual financial statements data.
        
        Combines income statement, balance sheet, and cash flow data for yearly periods.
        """
        self.logger.info(f"Extracting yearly financials for {symbol}")
        stock = self._getTicker(symbol)
        # Join all three financial statements for comprehensive annual data
        df = self._join_financial_statements(
            stock.financials.transpose(),
            stock.balance_sheet.transpose(),
            stock.cashflow.transpose()
        )
        if df.empty:
            self.logger.warning(f"No yearly financials found for {symbol}")
        return self._df_to_json_safe(df)
    
    def extract_market_data(self, symbol: str, period: str = "5y", interval: str = "1d") -> List[Dict[str, Any]]:
        """Extract historical price and volume data.
        
        Returns OHLCV (Open, High, Low, Close, Volume) data for specified period and interval.
        """
        self.logger.info(f"Extracting market data for {symbol} (period={period}, interval={interval})")
        stock = self._getTicker(symbol)
        # Get historical price data with auto-adjusted prices for splits/dividends
        df = stock.history(period=period, interval=interval, auto_adjust=True).reset_index()
        if df.empty:
            self.logger.warning(f"No market data found for {symbol}")
        return self._df_to_json_safe(df)
    
    def extract_corporate_actions(self, symbol: str) -> List[Dict[str, Any]]:
        """Extract corporate actions data (dividends, stock splits).
        
        Returns historical dividend payments and stock split information.
        """
        self.logger.info(f"Extracting corporate actions data for {symbol}")
        stock = self._getTicker(symbol)
        # Get dividend and stock split history
        df = stock.actions
        if df.empty:
            self.logger.warning(f"No corporate action data found for {symbol}")
        return self._df_to_json_safe(df)
    
    def extract_recommendations(self, symbol: str) -> List[Dict[str, Any]]:
        """Extract analyst recommendations summary.
        
        Returns buy/hold/sell recommendations from financial analysts.
        """
        self.logger.info(f"Extracting recommendations data for {symbol}")
        stock = self._getTicker(symbol)
        # Get analyst recommendation summary (buy/hold/sell counts)
        df = stock.recommendations_summary
        if df.empty:
            self.logger.warning(f"No recommendations found for {symbol}")
        return self._df_to_json_safe(df)
    
    def extract_revisions(self, symbol: str) -> List[Dict[str, Any]]:
        """Extract analyst upgrades and downgrades history.
        
        Returns historical analyst rating changes (upgrades/downgrades).
        """
        self.logger.info(f"Extracting revisions data for {symbol}")
        stock = self._getTicker(symbol)
        # Get analyst upgrades/downgrades history
        df = stock.upgrades_downgrades
        if df.empty:
            self.logger.warning(f"No revisions found for {symbol}")
        return self._df_to_json_safe(df)
    
    def extract_price_targets(self, symbol: str) -> Dict[str, Any]:
        """Extract analyst price targets.
        
        Returns current analyst price targets (high, low, mean, median).
        """
        self.logger.info(f"Extracting price targets data for {symbol}")
        stock = self._getTicker(symbol)
        # Get analyst price target consensus data
        result = stock.analyst_price_targets
        if not result or len(result) == 0:
            self.logger.warning(f"No price targets found for {symbol}")
        return result

    def extract_calendar(self, symbol: str) -> Dict[str, Any]:
        """Extract earnings calendar data.
        
        Returns upcoming earnings dates and estimates.
        """
        self.logger.info(f"Extracting calendar data for {symbol}")
        stock = self._getTicker(symbol)
        # Get earnings calendar with dates and estimates
        result = stock.calendar
        if not result or len(result) == 0:
            self.logger.warning(f"No calendar found for {symbol}")
        return result
    
    def extract_news(self, symbol: str) -> List[Dict[str, Any]]:
        """Extract recent news articles.
        
        Returns list of recent news articles related to the stock.
        """
        self.logger.info(f"Extracting news data for {symbol}")
        stock = self._getTicker(symbol)
        # Get recent news articles for the stock
        result = stock.news
        if not result or len(result) == 0:
            self.logger.warning(f"No news found for {symbol}")
        return result
    
    def extract_top_companies(self) -> List[Dict[str, Any]]:
        """Extract top companies by sector.
        
        Returns top performing companies organized by market sector.
        """
        self.logger.info(f"Extracting top companies")
        df = pd.DataFrame()
        # Iterate through all sectors to get top companies
        for s in self.sectors:
            sector_df = yf.Sector(s).top_companies
            if sector_df is not None and not sector_df.empty:
                sector_df["sector"] = s  # Add sector column for identification
                df = pd.concat([df, sector_df], ignore_index=True)
        return self._df_to_json_safe(df)
    
    def extract_top_etfs(self) -> Dict[str, Any]:
        """Extract top ETFs by sector.
        
        Returns top Exchange Traded Funds organized by market sector.
        """
        self.logger.info(f"Extracting top ETFs")
        result = {}
        # Get top ETFs for each sector
        for s in self.sectors:
            sector = yf.Sector(s).top_etfs
            if sector is not None:
                result[s] = sector  # Store ETFs by sector key
        return result
    
    def extract_top_funds(self) -> Dict[str, Any]:
        """Extract top mutual funds by sector.
        
        Returns top performing mutual funds organized by market sector.
        """
        self.logger.info(f"Extracting top Funds")
        result = {}
        # Get top mutual funds for each sector
        for s in self.sectors:
            sector = yf.Sector(s).top_mutual_funds
            if sector is not None:
                result[s] = sector  # Store funds by sector key
        return result
    
    def _getTicker(self, symbol: str) -> yf.Ticker:
        """Get Yahoo Finance ticker object with validation.
        
        Validates that the ticker symbol exists and has data.
        """
        result = yf.Ticker(symbol)
        # Validate ticker exists by checking if info has meaningful data
        if result is None or len(result.info) <= 1:
            raise ValueError("Symbol not found")
        return result
    
    def _join_financial_statements(self, income: pd.DataFrame, balance: pd.DataFrame, cash: pd.DataFrame) -> pd.DataFrame:
        """Join income, balance sheet, and cash flow statements."""
        return income.join(
            balance, how="outer", lsuffix="_income", rsuffix="_balance"
        ).join(
            cash, how="outer", rsuffix="_cashflow"
        ).reset_index().rename(columns={"index": "period"})
                
    def _df_to_json_safe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convert DataFrame to JSON-safe format.
        Handles NaN values and timestamp conversion for JSON serialization.
        """
        return [
            {col: (val.isoformat() if isinstance(val, pd.Timestamp) else None if pd.isna(val) else val)
            for col, val in row.items()}
            for row in df.to_dict(orient="records")
        ]
