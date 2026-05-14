from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core import security
from app.db.session import SessionLocal
from app import schemas

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(reusable_oauth2)
) -> schemas.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    # Mock user for now since we don't have a user table
    # In a real app, you would fetch from DB: user = crud.user.get(db, id=token_data.sub)
    if token_data.sub == "admin":
        return schemas.User(username="admin", role="admin", full_name="System Admin")
    elif token_data.sub == "analyst":
        return schemas.User(username="analyst", role="analyst", full_name="Fraud Analyst")
    
    raise HTTPException(status_code=404, detail="User not found")

def get_current_active_admin(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == settings.API_KEY:
        return api_key
    # We allow JWT or API Key
    return None
