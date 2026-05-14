from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.api.v1 import api_router
from app.utils.middleware import GlobalExceptionHandlerMiddleware
from app.utils.logger import logger

def create_app() -> FastAPI:
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI(
        title="FraudShield AI API",
        description="Production-grade Healthcare Claims Fraud Detection API",
        version="2.0.0",
        docs_url="/docs" if settings.API_V1_STR == "/api/v1" else None # Secure docs in prod
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Register Middleware
    app.add_middleware(GlobalExceptionHandlerMiddleware)

    # Register Routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up FraudShield AI Services...")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down FraudShield AI Services...")

    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "healthy", "version": "2.0.0"}

    return app

app = create_app()
