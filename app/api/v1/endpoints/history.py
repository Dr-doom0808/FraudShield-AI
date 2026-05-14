from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import fraud_service
from app.db.repository import fraud_repo

router = APIRouter()

@router.get("/")
def get_history(db: Session = Depends(get_db), limit: int = 100):
    """
    Get prediction history with associated claim data.
    """
    return fraud_service.get_prediction_history(db, limit)

@router.get("/claims")
def get_seeded_claims(db: Session = Depends(get_db), limit: int = 50):
    """
    Get sample claims from the database for easy loading.
    """
    return fraud_repo.get_seeded_claims(db, limit)

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get KPI statistics for the dashboard.
    """
    return fraud_service.get_dashboard_stats(db)

@router.get("/analytics")
def get_advanced_analytics(db: Session = Depends(get_db)):
    """
    Get advanced analytics for the dataset.
    """
    return fraud_service.get_advanced_analytics(db)
