from fastapi import FastAPI
from .api import stocks_router

app = FastAPI(title="Stock Market Simulator")

app.include_router(stocks_router)


@app.get("/", tags=["health"])
def read_root():
    return {"message": "Stock Market application backend is running!"}
