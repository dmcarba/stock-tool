import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from stock_tool.routers.stock_extraction_router import StockExtractionRouter

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

@pytest.fixture
def client():
    router_instance = StockExtractionRouter()
    app = FastAPI()
    app.include_router(router_instance.router)
    return TestClient(app)


def test_get_ticker_info(client):
    """Integration test with real Yahoo Finance API"""
    response = client.get("/stock/info/AAPL")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["symbol"] == "AAPL"
    assert "longName" in data
    assert "marketCap" in data
    assert "sector" in data


def test_get_ticker_info_invalid_symbol(client):
    """Test with invalid symbol - should return real API error or empty data"""
    response = client.get("/stock/info/INVALIDTICKER123")
    
    print(response.json())
    # May return 200 with empty data or 404 depending on yfinance behavior
    assert response.status_code in [200, 404]


def test_get_quarterly_financials(client):
    """Integration test for quarterly financials with real API"""
    response = client.get("/stock/quarterly-financials/AAPL")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "period" in data[0]
    assert isinstance(data[0], dict)


def test_get_yearly_financials(client):
    """Integration test for yearly financials with real API"""
    response = client.get("/stock/yearly-financials/AAPL")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "period" in data[0]
    assert isinstance(data[0], dict)


def test_get_market_data(client):
    """Integration test for technical data with real API"""
    response = client.get("/stock/market/AAPL?period=1mo&interval=1d")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)
    assert "Date" in data[0] or "Datetime" in data[0]
    assert "Close" in data[0]
    assert "Volume" in data[0]


@pytest.mark.parametrize("ticker", ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"])
def test_multiple_tickers_info(client, ticker):
    """Test ticker info for 5 different stocks"""
    response = client.get(f"/stock/info/{ticker}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == ticker
    assert "longName" in data


@pytest.mark.parametrize("ticker", ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"])
def test_multiple_tickers_quarterly_financials(client, ticker):
    """Test quarterly financials for 5 different stocks"""
    response = client.get(f"/stock/quarterly-financials/{ticker}")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.parametrize("ticker", ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"])
def test_multiple_tickers_market_data(client, ticker):
    """Test technical data for 5 different stocks"""
    response = client.get(f"/stock/market/{ticker}?period=1mo&interval=1d")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_invalid_ticker_info(client):
    """Test ticker info with invalid symbol returns 404"""
    response = client.get("/stock/info/INVALIDTICKER999")
        
    assert response.status_code == 404
    assert response.json()["detail"] == "Symbol not found"


def test_invalid_quarterly_financials(client):
    """Test quarterly financials with symbol that has no data"""
    response = client.get("/stock/quarterly-financials/INVALIDTICKER999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Symbol not found"


def test_invalid_yearly_financials(client):
    """Test yearly financials with symbol that has no data"""
    response = client.get("/stock/yearly-financials/INVALIDTICKER999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Symbol not found"


def test_invalid_market_data(client):
    """Test technical data with symbol that has no data"""
    response = client.get("/stock/market/INVALIDTICKER999?period=1mo&interval=1d")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Symbol not found"


def test_get_corporate_actions(client):
    """Integration test for corporate actions with real API"""
    response = client.get("/stock/corporate-actions/AAPL")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_recommendations(client):
    """Integration test for recommendations with real API"""
    response = client.get("/stock/recommendations/AAPL")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_revisions(client):
    """Integration test for revisions with real API"""
    response = client.get("/stock/revisions/AAPL")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_price_targets(client):
    """Integration test for price targets with real API"""
    response = client.get("/stock/price-targets/AAPL")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_get_calendar(client):
    """Integration test for calendar with real API"""
    response = client.get("/stock/calendar/AAPL")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_get_news(client):
    """Integration test for news with real API"""
    response = client.get("/stock/news/AAPL")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_top_companies(client):
    """Integration test for top companies with real API"""
    response = client.get("/stock/top-companies")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_top_etfs(client):
    """Integration test for top ETFs with real API"""
    response = client.get("/stock/top-etfs")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_get_top_funds(client):
    """Integration test for top funds with real API"""
    response = client.get("/stock/top-funds")
    
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


def test_extract_listing_summary(client):
    """Test extract listing summary endpoint"""
    symbols = ["AAPL", "GOOGL", "MSFT"]
    response = client.post("/stock/listing-summary", json=symbols)
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "symbol" in data[0]