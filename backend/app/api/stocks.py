from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from ..schemas import StockTrade, Portfolio