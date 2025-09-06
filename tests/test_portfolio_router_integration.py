"""Integration tests for portfolio router."""

import pytest
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI
from stock_tool.routers.portfolio_router import PortfolioRouter


@pytest.fixture
def client():
    # Use test database
    os.environ["PORTFOLIO_DB_PATH"] = "test_portfolio.db"
    router_instance = PortfolioRouter()
    app = FastAPI()
    app.include_router(router_instance.router)
    yield TestClient(app)
    
    # Cleanup test database
    if os.path.exists("test_portfolio.db"):
        os.remove("test_portfolio.db")


def test_get_empty_portfolio(client):
    """Test getting empty portfolio initially."""
    response = client.get("/portfolio/tickers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_add_ticker(client):
    """Test adding a ticker to portfolio."""
    ticker_data = [{"symbol": "AAPL", "quantity": 10.0}]
    response = client.post("/portfolio/tickers", json=ticker_data)
    print(response.json())
    assert response.status_code == 200


def test_get_ticker_after_add(client):
    """Test getting specific ticker after adding."""
    # Add ticker first
    ticker_data = [{"symbol": "GOOGL", "quantity": 5.0}]
    client.post("/portfolio/tickers", json=ticker_data)
    
    # Get specific ticker
    response = client.get("/portfolio/tickers/GOOGL")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "GOOGL"
    assert data["quantity"] == 5.0


def test_get_all_tickers_after_add(client):
    """Test getting all tickers after adding multiple."""
    # Add multiple tickers
    ticker_data = [
        {"symbol": "MSFT", "quantity": 15.0},
        {"symbol": "TSLA", "quantity": 3.0}
    ]
    client.post("/portfolio/tickers", json=ticker_data)
    
    # Get all tickers
    response = client.get("/portfolio/tickers")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    symbols = [ticker["symbol"] for ticker in data]
    assert "MSFT" in symbols
    assert "TSLA" in symbols


def test_update_ticker_quantity(client):
    """Test updating ticker quantity."""
    # Add ticker
    ticker_data = [{"symbol": "AMZN", "quantity": 2.0}]
    client.post("/portfolio/tickers", json=ticker_data)
    
    # Update quantity
    updated_data = [{"symbol": "AMZN", "quantity": 5.0}]
    response = client.post("/portfolio/tickers", json=updated_data)
    assert response.status_code == 200
    
    # Verify update
    response = client.get("/portfolio/tickers/AMZN")
    assert response.status_code == 200
    assert response.json()["quantity"] == 5.0


def test_delete_ticker(client):
    """Test deleting a ticker from portfolio."""
    # Add ticker first
    ticker_data = [{"symbol": "NVDA", "quantity": 8.0}]
    client.post("/portfolio/tickers", json=ticker_data)
    
    # Delete ticker
    response = client.delete("/portfolio/tickers/NVDA")
    assert response.status_code == 200


def test_get_deleted_ticker_returns_404(client):
    """Test getting deleted ticker returns 404."""
    # Add and then delete ticker
    ticker_data = [{"symbol": "META", "quantity": 12.0}]
    client.post("/portfolio/tickers", json=ticker_data)
    client.delete("/portfolio/tickers/META")
    
    # Try to get deleted ticker
    response = client.get("/portfolio/tickers/META")
    assert response.status_code == 404


def test_delete_nonexistent_ticker_returns_404(client):
    """Test deleting non-existent ticker returns 404."""
    response = client.delete("/portfolio/tickers/NONEXISTENT")
    assert response.status_code == 404


def test_get_nonexistent_ticker_returns_404(client):
    """Test getting non-existent ticker returns 404."""
    response = client.get("/portfolio/tickers/NONEXISTENT")
    assert response.status_code == 404


def test_add_invalid_ticker_data(client):
    """Test adding invalid ticker data returns 500."""
    # Missing required fields
    invalid_data = [{"symbol": "AAPL"}]  # Missing quantity
    response = client.post("/portfolio/tickers", json=invalid_data)
    assert response.status_code == 422  # Validation error


def test_portfolio_workflow(client):
    """Test complete portfolio workflow."""
    # Start with empty portfolio
    response = client.get("/portfolio/tickers")
    initial_count = len(response.json())
    
    # Add multiple tickers
    tickers = [
        {"symbol": "AAPL", "quantity": 10.0},
        {"symbol": "GOOGL", "quantity": 5.0},
        {"symbol": "MSFT", "quantity": 15.0}
    ]
    response = client.post("/portfolio/tickers", json=tickers)
    assert response.status_code == 200
    
    # Verify all added
    response = client.get("/portfolio/tickers")
    assert len(response.json()) == initial_count + 3
    
    # Update one ticker
    updated = [{"symbol": "AAPL", "quantity": 20.0}]
    client.post("/portfolio/tickers", json=updated)
    
    # Verify update
    response = client.get("/portfolio/tickers/AAPL")
    assert response.json()["quantity"] == 20.0
    
    # Delete one ticker
    response = client.delete("/portfolio/tickers/GOOGL")
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get("/portfolio/tickers")
    symbols = [t["symbol"] for t in response.json()]
    assert "GOOGL" not in symbols
    assert len(response.json()) == initial_count + 2