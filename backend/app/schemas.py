from pydantic import BaseModel, Field

# Porfolio Schemas
class Holding(BaseModel):
    """Represents a single stock holding in the portfolio."""
    symbol: str
    shares: int = Field(..., gt=0, description="Number of shares held")
    average_price: float = Field(..., gt=0, description="Average purchase price per share")

class Portfolio(BaseModel):
    """Represent the user's complete porfolio."""
    cash: float = Field(..., gt=0, description="Available cash for trading")

# Session Schemas
class SessionData(BaseModel):
    """Represents the data stored in the user session."""
    portfolio: Portfolio = Field(default_factory=Portfolio)

# Stock Trading Schemas
class StockTrade(BaseModel):
    """Represents the stock buy or sell requests."""
    symbol: str
    shares: int = Field(..., gt=0, description="Number of shares to trade.")
