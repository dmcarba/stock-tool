import pytest
import pytest_asyncio
import asyncio
import time
import docker
import requests
from fastmcp import Client

@pytest.fixture(scope="module")
def docker_container():
    """Build and start Docker container for testing"""
    client = docker.from_env()
    
    image_tag = "stock-tool:test"
    
    # Always remove existing image first
    try:
        client.images.remove(image=image_tag, force=True)
        print(f"Removed existing image: {image_tag}")
    except docker.errors.ImageNotFound:
        print("No existing image found")
        
    _,_ = client.images.build(path=".", tag=image_tag, rm=True)
    
    # Log image size
    image = client.images.get(image_tag)
    size_mb = image.attrs['Size'] / (1024 * 1024)
    print(f"Image size: {size_mb:.2f} MB")

    print("starting container")
    # Start container with both MCP and API servers
    container = client.containers.run(
        image_tag,
        ports={"3001/tcp": 3001, "8001/tcp": 8001},
        detach=True,
        name="stock-tool-test"
    )
    
    # Wait for container to start
    timeout = 30
    interval = 1
    start_time = time.time()
    while True:
        container.reload()  # refresh status
        print(f"Container status: {container.status}")
        if container.status == "running":
            break
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Container {container.name} did not start within {timeout} seconds")
        time.sleep(interval)
        
    yield container
    
    # Cleanup
    try:
        container.stop()
        container.remove()
        client.images.remove(image=image_tag, force=True)
        print("Docker cleanup completed")
    except Exception as e:
        print(f"Cleanup error: {e}")

@pytest.fixture(autouse=True)
def cleanup_portfolio_db(docker_container):
    """Clear portfolio database between tests."""
    yield
    # Clear all portfolio data after each test
    try:
        response = requests.get("http://localhost:8001/portfolio/tickers", timeout=10)
        if response.status_code == 200:
            tickers = response.json()
            for ticker in tickers:
                requests.delete(f"http://localhost:8001/portfolio/tickers/{ticker['symbol']}", timeout=10)
    except Exception:
        pass  # Ignore cleanup errors

@pytest_asyncio.fixture
async def mcp_client(docker_container):
    """Create MCP client for testing."""
    for attempt in range(10):
        try:
            async with Client("http://127.0.0.1:3001/mcp") as client:
                print(await client.list_tools())
                yield client
                return
        except Exception as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < 9:
                await asyncio.sleep(1)
            else:
                raise

@pytest.mark.asyncio
async def test_mcp_ticker_info_endpoint(mcp_client):
    """Test MCP ticker info endpoint"""
    result = await mcp_client.call_tool("get_ticker_info", {"symbol": "AAPL"})
    print(f"Ticker info result: {result}")
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_market_data_endpoint(mcp_client):
    """Test MCP market data endpoint"""
    result = await mcp_client.call_tool("get_market_data", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_quarterly_financials_endpoint(mcp_client):
    """Test MCP quarterly financials endpoint"""
    result = await mcp_client.call_tool("get_quarterly_financials", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_yearly_financials_endpoint(mcp_client):
    """Test MCP yearly financials endpoint"""
    result = await mcp_client.call_tool("get_yearly_financials", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_corporate_actions_endpoint(mcp_client):
    """Test MCP corporate actions endpoint"""
    result = await mcp_client.call_tool("get_corporate_actions", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_recommendations_endpoint(mcp_client):
    """Test MCP recommendations endpoint"""
    result = await mcp_client.call_tool("get_recommendations", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_revisions_endpoint(mcp_client):
    """Test MCP revisions endpoint"""
    result = await mcp_client.call_tool("get_revisions", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_price_targets_endpoint(mcp_client):
    """Test MCP price targets endpoint"""
    result = await mcp_client.call_tool("get_price_targets", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_calendar_endpoint(mcp_client):
    """Test MCP calendar endpoint"""
    result = await mcp_client.call_tool("get_calendar", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_news_endpoint(mcp_client):
    """Test MCP news endpoint"""
    result = await mcp_client.call_tool("get_news", {"symbol": "AAPL"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_top_companies_endpoint(mcp_client):
    """Test MCP top companies endpoint"""
    result = await mcp_client.call_tool("get_top_companies", {})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_top_etfs_endpoint(mcp_client):
    """Test MCP top ETFs endpoint"""
    result = await mcp_client.call_tool("get_top_etfs", {})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_top_funds_endpoint(mcp_client):
    """Test MCP top funds endpoint"""
    result = await mcp_client.call_tool("get_top_funds", {})
    assert isinstance(result, list)
    assert len(result) > 0

# Portfolio MCP Tests
@pytest.mark.asyncio
async def test_mcp_add_tracked_ticker(mcp_client):
    """Test MCP add tracked ticker"""
    await mcp_client.call_tool("add_tracked_ticker", {"symbol": "AAPL", "quantity": 10.0})

@pytest.mark.asyncio
async def test_mcp_get_tracked_tickers(mcp_client):
    """Test MCP get tracked tickers"""
    await mcp_client.call_tool("add_tracked_ticker", {"symbol": "GOOGL", "quantity": 5.0})
    result = await mcp_client.call_tool("get_tracked_tickers", {})
    assert isinstance(result, list)

@pytest.mark.asyncio
async def test_mcp_remove_tracked_ticker(mcp_client):
    """Test MCP remove tracked ticker"""
    await mcp_client.call_tool("add_tracked_ticker", {"symbol": "TSLA", "quantity": 3.0})
    result = await mcp_client.call_tool("remove_tracked_ticker", {"symbol": "TSLA"})
    assert isinstance(result, list)

# Index Listing MCP Tests
@pytest.mark.asyncio
async def test_mcp_get_sp500_index(mcp_client):
    """Test MCP get S&P 500 index listing"""
    result = await mcp_client.call_tool("get_index_listing", {"index_name": "SP500"})
    assert isinstance(result, list)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_mcp_get_dax_index(mcp_client):
    """Test MCP get DAX index listing"""
    result = await mcp_client.call_tool("get_index_listing", {"index_name": "DAX"})
    assert isinstance(result, list)
    assert len(result) > 0

# REST API Tests
def test_rest_ticker_info(docker_container):
    """Test REST ticker info endpoint"""
    response = requests.get("http://localhost:8001/stock/info/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_rest_quarterly_financials(docker_container):
    """Test REST quarterly financials endpoint"""
    response = requests.get("http://localhost:8001/stock/quarterly-financials/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_yearly_financials(docker_container):
    """Test REST yearly financials endpoint"""
    response = requests.get("http://localhost:8001/stock/yearly-financials/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_market_data(docker_container):
    """Test REST market data endpoint"""
    response = requests.get("http://localhost:8001/stock/market/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_corporate_actions(docker_container):
    """Test REST corporate actions endpoint"""
    response = requests.get("http://localhost:8001/stock/corporate-actions/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_recommendations(docker_container):
    """Test REST recommendations endpoint"""
    response = requests.get("http://localhost:8001/stock/recommendations/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_revisions(docker_container):
    """Test REST revisions endpoint"""
    response = requests.get("http://localhost:8001/stock/revisions/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_price_targets(docker_container):
    """Test REST price targets endpoint"""
    response = requests.get("http://localhost:8001/stock/price-targets/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_rest_calendar(docker_container):
    """Test REST calendar endpoint"""
    response = requests.get("http://localhost:8001/stock/calendar/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_rest_news(docker_container):
    """Test REST news endpoint"""
    response = requests.get("http://localhost:8001/stock/news/AAPL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_top_companies(docker_container):
    """Test REST top companies endpoint"""
    response = requests.get("http://localhost:8001/stock/top-companies", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_top_etfs(docker_container):
    """Test REST top ETFs endpoint"""
    response = requests.get("http://localhost:8001/stock/top-etfs", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_rest_top_funds(docker_container):
    """Test REST top funds endpoint"""
    response = requests.get("http://localhost:8001/stock/top-funds", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

# Portfolio REST API Tests
def test_rest_portfolio_get_empty(docker_container):
    """Test REST portfolio get empty tickers"""
    response = requests.get("http://localhost:8001/portfolio/tickers", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_rest_portfolio_add_ticker(docker_container):
    """Test REST portfolio add ticker"""
    ticker_data = [{"symbol": "AAPL", "quantity": 10.0}]
    response = requests.post("http://localhost:8001/portfolio/tickers", json=ticker_data, timeout=30)
    assert response.status_code == 200

def test_rest_portfolio_get_ticker(docker_container):
    """Test REST portfolio get specific ticker"""
    ticker_data = [{"symbol": "GOOGL", "quantity": 5.0}]
    requests.post("http://localhost:8001/portfolio/tickers", json=ticker_data, timeout=30)
    
    response = requests.get("http://localhost:8001/portfolio/tickers/GOOGL", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "GOOGL"
    assert data["quantity"] == 5.0

def test_rest_portfolio_delete_ticker(docker_container):
    """Test REST portfolio delete ticker"""
    ticker_data = [{"symbol": "MSFT", "quantity": 15.0}]
    requests.post("http://localhost:8001/portfolio/tickers", json=ticker_data, timeout=30)
    
    response = requests.delete("http://localhost:8001/portfolio/tickers/MSFT", timeout=30)
    assert response.status_code == 200
    assert response.json() is True

# Index Listing REST API Tests
def test_rest_get_sp500_index(docker_container):
    """Test REST get S&P 500 index listing"""
    response = requests.get("http://localhost:8001/indices/SP500", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_get_dax_index(docker_container):
    """Test REST get DAX index listing"""
    response = requests.get("http://localhost:8001/indices/DAX", timeout=30)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_rest_get_invalid_index(docker_container):
    """Test REST get invalid index returns 404"""
    response = requests.get("http://localhost:8001/indices/INVALID", timeout=30)
    assert response.status_code == 404

    