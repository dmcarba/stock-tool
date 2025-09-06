from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, Dict

class Ticker(BaseModel):
    symbol: str
    quantity: float
    createad_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    
class TickerSummary(BaseModel):
    # ----------------------------
    # Basic identification
    # ----------------------------
    symbol: str  # Stock ticker symbol, e.g., "AAPL"
    name: Optional[str] = None  # Company short name or long name

    # --- Price & Multiples ---
    currentPrice: Optional[float] = None  # Current market price
    trailingPE: Optional[float] = None  # Trailing P/E ratio
    forwardPE: Optional[float] = None  # Forward P/E ratio
    priceToBook: Optional[float] = None  # Price-to-book ratio
    enterpriseToEbitda: Optional[float] = None  # Enterprise value / EBITDA ratio

    # --- Earnings & Growth ---
    epsTrailingTwelveMonths: Optional[float] = None  # Trailing 12-month EPS
    epsForward: Optional[float] = None  # Forward EPS estimate
    revenueGrowth: Optional[float] = None  # Revenue growth rate (decimal)
    earningsGrowth: Optional[float] = None  # Earnings growth rate (decimal)

    # --- Profitability ---
    returnOnEquity: Optional[float] = None  # ROE %
    profitMargins: Optional[float] = None  # Profit margin %

    # --- Cash & Debt ---
    freeCashflow: Optional[int] = None  # Free cash flow
    totalDebt: Optional[int] = None  # Total debt
    totalCash: Optional[int] = None  # Total cash
    debtToEquity: Optional[float] = None  # Debt/Equity ratio

    # --- Dividends ---
    dividendRate: Optional[float] = None  # Annual dividend rate
    dividendYield: Optional[float] = None  # Dividend yield %
    payoutRatio: Optional[float] = None  # Dividend payout ratio
    dividendGrowth5Y: Optional[float] = None  # 5-year dividend growth %

    # --- Market / Analyst ---
    targetMeanPrice: Optional[float] = None  # Average analyst target price
    recommendationKey: Optional[str] = None  # Analyst recommendation (buy/hold/sell)
    recommendationMean: Optional[float] = None  # Numerical mean recommendation
    averageAnalystRating: Optional[str] = None  # Summary of analyst ratings
    recommendationBreakdown: Optional[Dict[str,int]] = None  
    # Structured dictionary of most recent recommendations
    # e.g., {"strongBuy": 5, "buy": 23, "hold": 14, "sell": 1, "strongSell": 2}

    # --- Computed ---
    discountToTarget: Optional[float] = None  
    # (TargetPrice - CurrentPrice)/TargetPrice
    pegRatio: Optional[float] = None  # Forward P/E / Earnings Growth
    undervaluation_score: Optional[float] = None  # Weighted score of undervaluation

    # ----------------------------
    # Validators for computed fields
    # ----------------------------
    @field_validator("discountToTarget")
    def compute_discount(cls, v, values):
        price = values.get("currentPrice")
        target = values.get("targetMeanPrice")
        if price and target and target != 0:
            return (target - price) / target
        return None

    @field_validator("pegRatio")
    def compute_peg(cls, v, values):
        fpe = values.get("forwardPE")
        growth = values.get("earningsGrowth")
        if fpe and growth and growth != 0:
            return fpe / growth
        return None

    @field_validator("undervaluation_score")
    def compute_score(cls, v, values):
        """
        Compute composite undervaluation score using weighted metrics:
        - discount to target price
        - PEG ratio
        - P/E ratio (benchmark 15)
        - dividend yield
        """
        weights = {"discount":0.4, "peg":0.3, "pe":0.2, "dividend":0.1}
        score = 0.0
        discount = values.get("discountToTarget")
        peg = values.get("pegRatio")
        pe = values.get("trailingPE")
        dy = values.get("dividendYield")
        if discount is not None:
            score += min(max(discount*100,0),100) * weights["discount"]
        if peg is not None and peg > 0:
            score += min(max((1/peg)*100,0),100) * weights["peg"]
        if pe is not None and pe > 0:
            score += min(max((15/pe)*100,0),100) * weights["pe"]
        if dy is not None:
            score += min(max(dy*100,0),100) * weights["dividend"]
        return round(score,2)
