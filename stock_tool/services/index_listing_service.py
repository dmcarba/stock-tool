import pandas as pd
import requests
from io import StringIO
from typing import List

class IndexListingService:
    
    indices = {
    "SP500": {"url": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", "suffix": None},
    "IBEX35": {"url": "https://en.wikipedia.org/wiki/IBEX_35", "suffix": None},
    "FTSE100": {"url": "https://en.wikipedia.org/wiki/FTSE_100_Index", "suffix": "L"},
    "DAX": {"url": "https://en.wikipedia.org/wiki/DAX", "suffix": None},
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    
    possible_columns = ["Symbol", "Ticker", "EPIC", "Code", "ISIN"]

    
    def __init__(self) -> None:
        pass
    
    def get_index_listing(self, index_name: str) -> List[str]:
        
        if index_name not in self.indices:
            raise ValueError(f"Index {index_name} not supported")
        
        url = self.indices[index_name]["url"]
        suffix = self.indices[index_name]["suffix"]

        response = requests.get(url, headers = self.headers)
        response.raise_for_status()

        tables = pd.read_html(StringIO(response.text))

        if len(tables) == 0:
            raise ValueError("No tables found on the page")
    
        symbols = []
        # Scan all tables for a valid ticker column
        for df in tables:
            for col in self.possible_columns:
                if col in df.columns:
                    symbols = df[col].tolist()
                    break
            if symbols:
                break
    
        if not symbols:
            raise ValueError("No ticker column found in any table on the page")
    
        for i in range(len(symbols)):
            symbols[i] = symbols[i].strip()  # elimina espacios
            if suffix:
                symbols[i] += "." + suffix
    
        return symbols
   