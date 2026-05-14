from fastapi import APIRouter, Depends
from .endpoints import predict, history, auth
from app.api.deps import get_api_key

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(predict.router, prefix="/predict", tags=["predict"], dependencies=[Depends(get_api_key)])
api_router.include_router(history.router, prefix="/history", tags=["history"], dependencies=[Depends(get_api_key)])
