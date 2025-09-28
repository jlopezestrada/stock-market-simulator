from enum import Enum
from pydantic import BaseModel, Field


# Holding Schema
class Holding(BaseModel):
    """Represents a single stock holding in the portfolio."""

    symbol: str
    shares: int = Field(..., gt=0, description="Number of shares held")
    average_price: float = Field(
        ..., gt=0, description="Average purchase price per share"
    )


# Portfolio Schema
class Portfolio(BaseModel):
    """Represent the user's complete porfolio."""

    cash: float = Field(default=1_000.0, gt=0, description="Available cash for trading")
    holdings: list[Holding] = Field(
        default_factory=list, description="Collection of stock holdings."
    )


# Session Schemas
class SessionData(BaseModel):
    """Represents the data stored in the user session."""

    portfolio: Portfolio = Field(default_factory=Portfolio)


# TradeType Schema
class TradeType(str, Enum):
    "Represent the trade operation type BUY or SELL"

    BUY = "buy"
    SELL = "sell"


# Stock Trading Schemas
class StockTrade(BaseModel):
    """Represents the stock buy or sell requests."""

    trade_type: TradeType = Field(..., description="Direction of the operation.")
    symbol: str
    shares: int = Field(..., gt=0, description="Number of shares to trade.")
    price_per_share: float = Field(
        ..., gt=0, description="Price used to evaluate the trade."
    )
