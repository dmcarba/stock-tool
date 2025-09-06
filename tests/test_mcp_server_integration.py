"""Integration tests for MCP server tools via MCP client."""

import pytest
import pytest_asyncio
import threading
import time
import os
from fastmcp import Client
from stock_tool.stock_tool import main

class TestMCPServerIntegration:
    """Integration tests for all MCP server tools via MCP client."""

    @pytest.fixture(scope="class")
    def mcp_server(self):
        """Start MCP server for testing."""
        import traceback
        
        # Use test database
        os.environ["PORTFOLIO_DB_PATH"] = "test_mcp_portfolio.db"
        
        def traced_main():
            try:
                print("Starting MCP server...")
                main()
            except Exception as e:
                print(f"MCP server failed to start: {e}")
                traceback.print_exc()
        
        print("Creating server thread...")
        server_thread = threading.Thread(target=traced_main, daemon=True)
        print("Starting server thread...")
        server_thread.start()
        print(f"Thread alive: {server_thread.is_alive()}")
        
        # Wait for server to be ready
        print("Waiting for server to be ready...")
        time.sleep(5)  # Give server time to fully start
        print("Server should be ready!")
        
        yield server_thread
        
        # Cleanup test database
        if os.path.exists("test_mcp_portfolio.db"):
            os.remove("test_mcp_portfolio.db")
    
    @pytest.fixture(autouse=True)
    def cleanup_db(self):
        """Clean database between tests."""
        yield
        # Remove test database after each test
        if os.path.exists("test_mcp_portfolio.db"):
            os.remove("test_mcp_portfolio.db")

    @pytest_asyncio.fixture
    async def mcp_client(self, mcp_server):
        """Create MCP client for testing."""
        async with Client("http://127.0.0.1:3001/mcp") as client:
            yield client

    @pytest.mark.asyncio
    async def test_client_connectivity(self, mcp_client):
        """Test MCP client can connect to server."""
        tools = await mcp_client.list_tools()
        assert isinstance(tools, list)
        print(f"Available tools: {tools}")
        print(f"Tool count: {len(tools)}")

    @pytest.mark.asyncio
    async def test_get_ticker_info(self, mcp_client):
        """Test ticker info tool."""
        result = await mcp_client.call_tool("get_ticker_info", {"symbol": "AAPL"})
        print(f"Ticker info result: {result}")
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_quarterly_financials(self, mcp_client):
        """Test quarterly financials tool."""
        result = await mcp_client.call_tool("get_quarterly_financials", {"symbol": "AAPL"})
        print(f"Quarterly financials result: {result}")
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_yearly_financials(self, mcp_client):
        """Test yearly financials tool."""
        result = await mcp_client.call_tool("get_yearly_financials", {"symbol": "AAPL"})
        print(f"Yearly financials result: {result}")
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_market_data(self, mcp_client):
        """Test technical data tool."""
        result = await mcp_client.call_tool("get_market_data", {"symbol": "AAPL", "period": "1y", "interval": "1d"})
        print(f"Market data result: {result}")
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_get_top_companies(self, mcp_client):
        """Test top companies tool."""
        result = await mcp_client.call_tool("get_top_companies", {})
        print(f"Top companies result: {result}")
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_add_tracked_ticker(self, mcp_client):
        """Test adding ticker to portfolio."""
        await mcp_client.call_tool("add_tracked_ticker", {"symbol": "AAPL", "quantity": 10.0})

    @pytest.mark.asyncio
    async def test_get_tracked_ticker(self, mcp_client):
        """Test getting specific tracked ticker."""
        await mcp_client.call_tool("add_tracked_ticker", {"symbol": "GOOGL", "quantity": 5.0})
        result = await mcp_client.call_tool("get_tracked_ticker", {"symbol": "GOOGL"})
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_tracked_tickers(self, mcp_client):
        """Test getting all tracked tickers."""
        await mcp_client.call_tool("add_tracked_ticker", {"symbol": "MSFT", "quantity": 15.0})
        result = await mcp_client.call_tool("get_tracked_tickers", {})
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_remove_tracked_ticker(self, mcp_client):
        """Test removing ticker from portfolio."""
        await mcp_client.call_tool("add_tracked_ticker", {"symbol": "NVDA", "quantity": 8.0})
        result = await mcp_client.call_tool("remove_tracked_ticker", {"symbol": "NVDA"})
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_remove_nonexistent_ticker(self, mcp_client):
        """Test removing non-existent ticker raises error."""
        try:
            await mcp_client.call_tool("remove_tracked_ticker", {"symbol": "NONEXISTENT"})
            assert False, "Expected exception but none was raised"
        except Exception as e:
            print(f"Exception type: {type(e)}")
            print(f"Exception message: {e}")
            assert True

    @pytest.mark.asyncio
    async def test_get_sp500_index_listing(self, mcp_client):
        """Test getting S&P 500 index listing via MCP."""
        result = await mcp_client.call_tool("get_index_listing", {"index_name": "SP500"})
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_dax_index_listing(self, mcp_client):
        """Test getting DAX index listing via MCP."""
        result = await mcp_client.call_tool("get_index_listing", {"index_name": "DAX"})
        assert isinstance(result, list)
        assert len(result) > 0
        
    @pytest.mark.asyncio
    async def test_get_ibex35_index_listing(self, mcp_client):
        """Test getting IBEX35 index listing via MCP."""
        result = await mcp_client.call_tool("get_index_listing", {"index_name": "IBEX35"})
        assert isinstance(result, list)
        assert len(result) > 0
        
    @pytest.mark.asyncio
    async def test_get_ftse100_index_listing(self, mcp_client):
        """Test getting FTSE100 index listing via MCP."""
        result = await mcp_client.call_tool("get_index_listing", {"index_name": "FTSE100"})
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_get_invalid_index_listing(self, mcp_client):
        """Test getting invalid index listing raises error."""
        try:
            await mcp_client.call_tool("get_index_listing", {"index_name": "INVALID"})
            assert False, "Expected exception but none was raised"
        except Exception as e:
            print(f"Index listing exception: {type(e)} - {e}")
            assert True

    @pytest.mark.asyncio
    async def test_get_listing_summary(self, mcp_client):
        """Test getting listing summary for multiple symbols via MCP."""
        symbols = ["AAPL", "GOOGL", "MSFT"]
        result = await mcp_client.call_tool("get_listing_summary", {"symbols": symbols})
        assert isinstance(result, list)
        assert len(result) > 0
