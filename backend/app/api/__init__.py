# Expose API routers to the application
from .stocks import router as stocks_router

__all__ = ["stocks_router"]
