"""MCP Server module for stock data extraction."""

from typing import Dict, List, Any
from .services.stock_extraction_service import StockExtractionService
from .services.portfolio_service import PortfolioService
from .services.index_listing_service import IndexListingService
from mcp.server.fastmcp import FastMCP
import os

mcp_port = int(os.environ.get("MCP_PORT", 3001))
mcp = FastMCP("Stock tool MCP Server", log_level="ERROR", port=mcp_port, stateless_http=True, host="0.0.0.0")
service = StockExtractionService()
portfolio_service = PortfolioService()
index_service = IndexListingService()

def start_mcp_server():
    """Start the MCP server."""
    print(f"Starting MCP server on port {mcp_port}...")
    mcp.run(transport='streamable-http')
    
@mcp.tool(description="Get comprehensive ticker information including company details, market cap, sector, and key financial metrics")
def get_ticker_info(symbol: str) -> Dict[str, Any]:
    """Get basic ticker information."""
    return service.extract_ticker_info(symbol)
    
@mcp.tool(description="Retrieve quarterly financial statements including income statement, balance sheet, and cash flow data")
def get_quarterly_financials(symbol: str) -> List[Dict[str, Any]]:
    """Get quarterly financial statements."""
    return service.extract_quarterly_financials(symbol)
    
@mcp.tool(description="Retrieve annual financial statements including income statement, balance sheet, and cash flow data")
def get_yearly_financials(symbol: str) -> List[Dict[str, Any]]:
    """Get yearly financial statements."""
    return service.extract_yearly_financials(symbol)
    
@mcp.tool(description="Get historical stock price data including open, high, low, close, and volume for market analysis")
def get_market_data(symbol: str, period: str = "5y", interval: str = "1d") -> List[Dict[str, Any]]:
    """Get historical price and volume data."""
    return service.extract_market_data(symbol, period, interval)
    
@mcp.tool(description="Retrieve corporate actions history including dividend payments, stock splits, and other shareholder events")
def get_corporate_actions(symbol: str) -> List[Dict[str, Any]]:
    """Get corporate actions (dividends, splits)."""
    return service.extract_corporate_actions(symbol)
    
@mcp.tool(description="Get current analyst recommendations and ratings (buy, hold, sell) from financial institutions")
def get_recommendations(symbol: str) -> List[Dict[str, Any]]:
    """Get analyst recommendations."""
    return service.extract_recommendations(symbol)
    
@mcp.tool(description="Get recent analyst rating changes including upgrades, downgrades, and target price revisions")
def get_revisions(symbol: str) -> List[Dict[str, Any]]:
    """Get analyst upgrades/downgrades."""
    return service.extract_revisions(symbol)
    
@mcp.tool(description="Get analyst price targets including mean, high, low, and current target prices")
def get_price_targets(symbol: str) -> Dict[str, Any]:
    """Get analyst price targets."""
    return service.extract_price_targets(symbol)
    
@mcp.tool(description="Get upcoming earnings calendar with expected earnings dates and estimates")
def get_calendar(symbol: str) -> Dict[str, Any]:
    """Get earnings calendar."""
    return service.extract_calendar(symbol)
    
@mcp.tool(description="Get recent news articles and updates for a stock symbol")
def get_news(symbol: str) -> List[Dict[str, Any]]:
    """Get recent news articles."""
    return service.extract_news(symbol)
    
@mcp.tool(description="Get list of top performing companies organized by market sector and industry")
def get_top_companies() -> List[Dict[str, Any]]:
    """Get top companies by sector."""
    return service.extract_top_companies()
    
@mcp.tool(description="Get top performing Exchange Traded Funds (ETFs) categorized by sector and investment focus")
def get_top_etfs() -> Dict[str, Any]:
    """Get top ETFs by sector."""
    return service.extract_top_etfs()
    
@mcp.tool(description="Get top performing mutual funds organized by investment category and sector focus")
def get_top_funds() -> Dict[str, Any]:
    """Get top mutual funds by sector."""
    return service.extract_top_funds()

@mcp.tool(description="Get all tracked tickers in portfolio")
def get_tracked_tickers() -> List[Dict[str, Any]]:
    """Get all tracked tickers."""
    tickers = portfolio_service.get_all_tracked_tickers()
    return [ticker.model_dump() for ticker in tickers]

@mcp.tool(description="Get specific portfolio tracked ticker by symbol")
def get_tracked_ticker(symbol: str) -> Dict[str, Any]:
    """Get tracked ticker by symbol."""
    ticker = portfolio_service.get_tracked_ticker(symbol)
    return ticker.model_dump()

@mcp.tool(description="Add ticker to portfolio tracking")
def add_tracked_ticker(symbol: str, quantity: float):
    """Add ticker to portfolio."""
    portfolio_service.add_ticker(symbol, quantity)

@mcp.tool(description="Remove ticker from portfolio tracking")
def remove_tracked_ticker(symbol: str):
    """Remove ticker from portfolio."""
    portfolio_service.remove_ticker(symbol)

@mcp.tool(description="Get stock symbols for a specific market index (SP500, IBEX35, FTSE100, DAX)")
def get_index_listing(index_name: str) -> List[str]:
    """Get stock symbols for a market index."""
    return index_service.get_index_listing(index_name)

@mcp.tool(description="Get comprehensive summary data for multiple stock symbols including current price, PE ratios, EPS, growth metrics, financial ratios, debt metrics, dividend information, analyst targets and recommendations")
def get_listing_summary(symbols: List[str]) -> List[Dict[str, Any]]:
    """Get listing summary for multiple symbols."""
    results = service.extract_listing_summary(symbols)
    return [result.model_dump() for result in results]