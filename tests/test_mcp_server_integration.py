"""Integration tests for MCP server tools via MCP client."""

import pytest
import pytest_asyncio
import threading
import time
from fastmcp import Client
from stock_tool.stock_tool import main

class TestMCPServerIntegration:
    """Integration tests for all MCP server tools via MCP client."""

    @pytest.fixture(scope="class")
    def mcp_server(self):
        """Start MCP server for testing."""
        import traceback
        
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