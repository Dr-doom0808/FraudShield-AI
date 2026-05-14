from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app import schemas
from app.services import fraud_service
from app.db.session import get_db

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=schemas.PredictionResult)
@limiter.limit("10/minute")
def predict_claim(
    request: Request,
    claim: schemas.Claim, 
    explain: bool = False, 
    db: Session = Depends(get_db)
):
    """
    Endpoint for single claim fraud analysis.
    """
    try:
        return fraud_service.process_prediction(db, claim, explain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch", response_model=list[schemas.PredictionResult])
@limiter.limit("2/minute")
def predict_batch(
    request: Request,
    claims: list[schemas.Claim], 
    db: Session = Depends(get_db)
):
    """
    Endpoint for auditing a batch of claims.
    """
    try:
        return fraud_service.process_batch_prediction(db, claims)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
