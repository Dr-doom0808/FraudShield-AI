from sqlalchemy.orm import Session
from app.db import models
from app import schemas

def create_claim(db: Session, claim: schemas.Claim):
    db_claim = models.Claim(**claim.dict())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

def create_prediction(db: Session, prediction_data: dict):
    db_prediction = models.Prediction(**prediction_data)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def get_history(db: Session, limit: int = 100):
    return db.query(models.Prediction, models.Claim)\
             .join(models.Claim, models.Prediction.claim_id == models.Claim.id)\
             .order_by(models.Prediction.created_at.desc())\
             .limit(limit).all()

def get_seeded_claims(db: Session, limit: int = 50):
    return db.query(models.Claim).limit(limit).all()

def get_stats(db: Session):
    total = db.query(models.Prediction).count()
    frauds = db.query(models.Prediction).filter(models.Prediction.is_fraud == True).count()
    return {"total": total, "frauds": frauds}
