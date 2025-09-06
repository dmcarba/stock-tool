"""Integration tests for index listing router."""

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from stock_tool.routers.index_listing_router import IndexListingRouter

@pytest.fixture
def client():
    router_instance = IndexListingRouter()
    app = FastAPI()
    app.include_router(router_instance.router)
    return TestClient(app)

def test_get_sp500_listing(client):
    """Test getting S&P 500 index listing."""
    response = client.get("/indices/SP500")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_dax_listing(client):
    """Test getting DAX index listing."""
    response = client.get("/indices/DAX")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_ftse100_listing(client):
    """Test getting FTSE 100 index listing."""
    response = client.get("/indices/FTSE100")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
def test_get_ibex35_listing(client):
    """Test getting IBEX 35 index listing."""
    response = client.get("/indices/IBEX35")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_invalid_index_returns_404(client):
    """Test getting invalid index returns 404."""
    response = client.get("/indices/INVALID")
    print(response.content)
    assert response.status_code == 404
