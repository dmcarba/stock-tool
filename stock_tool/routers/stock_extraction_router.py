from fastapi import APIRouter, HTTPException
import logging
from ..services.stock_extraction_service import StockExtractionService


class StockExtractionRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/stock", tags=["stock-extraction"])
        self.service = StockExtractionService()
        self.logger = logging.getLogger(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        self.router.get("/info/{symbol}", responses={404: {"description": "Symbol not found"}})(self.extract_ticker_info)
        self.router.get("/quarterly-financials/{symbol}", responses={404: {"description": "No quarterly data found"}})(self.extract_quarterly_financials)
        self.router.get("/yearly-financials/{symbol}", responses={404: {"description": "No yearly data found"}})(self.extract_yearly_financials)
        self.router.get("/market/{symbol}", responses={404: {"description": "No market data found"}})(self.extract_market_data)
        self.router.get("/corporate-actions/{symbol}", responses={404: {"description": "No corporate actions found"}})(self.extract_corporate_actions)
        self.router.get("/recommendations/{symbol}", responses={404: {"description": "No recommendations found"}})(self.extract_recommendations)
        self.router.get("/revisions/{symbol}", responses={404: {"description": "No revisions found"}})(self.extract_revisions)
        self.router.get("/price-targets/{symbol}", responses={404: {"description": "No price targets found"}})(self.extract_price_targets)
        self.router.get("/calendar/{symbol}", responses={404: {"description": "No calendar found"}})(self.extract_calendar)
        self.router.get("/news/{symbol}", responses={404: {"description": "No news found"}})(self.extract_news)
        self.router.get("/top-companies", responses={404: {"description": "No top companies found"}})(self.extract_top_companies)
        self.router.get("/top-etfs", responses={404: {"description": "No top ETFs found"}})(self.extract_top_etfs)
        self.router.get("/top-funds", responses={404: {"description": "No top funds found"}})(self.extract_top_funds)
        self.router.post("/listing-summary")(self.extract_listing_summary)
    
    def extract_ticker_info(self, symbol: str):
        try:
            return self.service.extract_ticker_info(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_ticker_info: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_quarterly_financials(self, symbol: str):
        try:
            return self.service.extract_quarterly_financials(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_quarterly_financials: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_yearly_financials(self, symbol: str):
        try:
            return self.service.extract_yearly_financials(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_yearly_financials: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_market_data(self, symbol: str, period: str = "5y", interval: str = "1d"):
        try:
            return self.service.extract_market_data(symbol, period, interval)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_market_data: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_corporate_actions(self, symbol: str):
        try:
            return self.service.extract_corporate_actions(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_corporate_actions: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_recommendations(self, symbol: str):
        try:
            return self.service.extract_recommendations(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_recommendations: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_revisions(self, symbol: str):
        try:
            return self.service.extract_revisions(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_revisions: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_price_targets(self, symbol: str):
        try:
            return self.service.extract_price_targets(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_price_targets: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_calendar(self, symbol: str):
        try:
            return self.service.extract_calendar(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_calendar: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_news(self, symbol: str):
        try:
            return self.service.extract_news(symbol)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_news: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_top_companies(self):
        try:
            return self.service.extract_top_companies()
        except ValueError as e:
            self.logger.error(f"ValueError in extract_top_companies: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_top_etfs(self):
        try:
            return self.service.extract_top_etfs()
        except ValueError as e:
            self.logger.error(f"ValueError in extract_top_etfs: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_top_funds(self):
        try:
            return self.service.extract_top_funds()
        except ValueError as e:
            self.logger.error(f"ValueError in extract_top_funds: {e}")
            raise HTTPException(status_code=404, detail=str(e))
    
    def extract_listing_summary(self, symbols: list[str]):
        try:
            return self.service.extract_listing_summary(symbols)
        except ValueError as e:
            self.logger.error(f"ValueError in extract_listing_summary: {e}")
            raise HTTPException(status_code=404, detail=str(e))

router = StockExtractionRouter().router

