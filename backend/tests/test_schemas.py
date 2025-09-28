import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.schemas import SessionData


def test_session_data_defaults():
    session = SessionData()

    assert session.portfolio.cash == 1_000.0
    assert session.portfolio.holdings == []
