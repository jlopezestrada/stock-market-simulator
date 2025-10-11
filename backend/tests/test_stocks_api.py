import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.api import stocks
from app.main import app
from app.schemas import StockTrade, TradeType


def setup_function(function):
    stocks._session_store.clear()


def test_router_is_registered():
    paths = {route.path for route in app.routes}
    assert "/stocks/sessions" in paths
    assert "/stocks/sessions/{session_id}/portfolio" in paths
    assert "/stocks/sessions/{session_id}/trade" in paths


def test_execute_sell_and_buy_trade():
    session_state = stocks.create_session()
    session_id = session_state.session_id

    buy_trade = StockTrade(
        symbol="NVDA", shares=5, trade_type=TradeType.BUY, price_per_share=183.00
    )
    portfolio_post_buy = stocks.execute_trade(session_id, buy_trade)
    portfolio = portfolio_post_buy.data.portfolio

    assert portfolio.cash == 85.00
    assert len(portfolio.holdings) == 1
    holding = portfolio.holdings[0]
    assert holding.symbol == "NVDA"
    assert holding.shares == 5
    assert holding.average_price == 183.00
