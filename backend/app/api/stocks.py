from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import Dict

from starlette.status import HTTP_400_BAD_REQUEST
from ..schemas import StockTrade, Portfolio, TradeType, SessionData, Holding

router = APIRouter(prefix="/stocks", tags=["stocks"])

_session_store: Dict[UUID, SessionData] = {}


def _get_session(session_id: UUID) -> SessionData:
    return _session_store[session_id]


def _apply_trade(portfolio: Portfolio, trade: StockTrade) -> None:
    symbol = trade.symbol.upper()
    shares = trade.shares
    price = trade.price_per_share

    existing: Holding | None = next(
        (holding for holding in portfolio.holdings if holding.symbol == symbol), None
    )

    # Check operation type BUY or SELL
    if trade.trade_type is TradeType.BUY:
        cost = shares * price
        if portfolio.cash < cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient cash to execute buy order.",
            )
        portfolio.cash -= cost
        if existing:
            total_shares = existing.shares + shares
            existing.average_price = (
                (existing.average_price * existing.shares) + cost
            ) / total_shares
            existing.shares = total_shares
        else:
            portfolio.holdings.append(
                Holding(symbol=symbol, shares=shares, average_price=price)
            )
        return

    # SELL
    if not existing or existing.shares < shares:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Insufficient shares to execute sell order.",
        )

    proceeds = shares * price
    existing.shares -= shares
    portfolio.cash += proceeds
    if existing.shares == 0:
        portfolio.holdings.remove(existing)
