from fastapi import APIRouter, HTTPException, status
from uuid import UUID, uuid4
from typing import Dict

from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK
from ..schemas import (
    StockTrade,
    Portfolio,
    TradeType,
    SessionData,
    SessionState,
    Holding,
)

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
    # BUY
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


@router.post("/sessions", status_code=HTTP_201_CREATED, response_model=SessionState)
def create_session() -> SessionState:
    session_id = uuid4()
    session_data = SessionData()
    _session_store[session_id] = session_data
    return SessionState(session_id=session_id, data=session_data)


@router.get("/sessions/{session_id}", response_model=SessionState)
def get_session(session_id: UUID) -> SessionState:
    session_data = _get_session(session_id)
    return SessionState(session_id=session_id, data=session_data)


@router.get(
    "/sessions/{session_id}/portfolio",
    status_code=HTTP_200_OK,
    response_model=Portfolio,
)
def get_portolio(session_id: UUID) -> Portfolio:
    session_data = _get_session(session_id)
    return session_data.portfolio


@router.post(
    "/sessions/{session_id}/trade", status_code=HTTP_200_OK, response_model=SessionState
)
def execute_trade(session_id: UUID, trade: StockTrade) -> SessionState:
    session_data = _get_session(session_id)
    _apply_trade(session_data.portfolio, trade)
    return SessionState(session_id=session_id, data=session_data)
