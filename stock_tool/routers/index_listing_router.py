"""Index listing router for market indices and sector listings."""

from fastapi import APIRouter, HTTPException
from typing import List
from ..services.index_listing_service import IndexListingService

class IndexListingRouter:
    def __init__(self) -> None:
        self.router = APIRouter(prefix="/indices", tags=["indices"])
        self.service = IndexListingService()
        self._setup_routes()
    
    def _setup_routes(self) -> None:
        self.router.get("/{index_name}", response_model=List[str])(self.get_index_listing)
    
    def get_index_listing(self, index_name: str) -> List[str]:
        """Get stock symbols for a specific index."""
        try:
            return self.service.get_index_listing(index_name)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get index listing: {str(e)}")


router = IndexListingRouter().router