from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    Provider = Column(String, index=True)
    InscClaimAmtReimbursed = Column(Float)
    IPAnnualReimbursementAmt = Column(Float)
    IPAnnualDeductibleAmt = Column(Float)
    TotalReimbursement = Column(Float)
    RenalDiseaseIndicator = Column(Integer)
    ChronicCond_Alzheimer = Column(Integer)
    ChronicCond_Heartfailure = Column(Integer)
    ChronicCond_KidneyDisease = Column(Integer)
    ChronicCond_Cancer = Column(Integer)
    ChronicCond_ObstrPulmonary = Column(Integer)
    ChronicCond_Depression = Column(Integer)
    ChronicCond_Diabetes = Column(Integer)
    ChronicCond_IschemicHeart = Column(Integer)
    ChronicCond_Osteoporasis = Column(Integer)
    ChronicCond_rheumatoidarthritis = Column(Integer)
    ChronicCond_stroke = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, index=True)
    is_fraud = Column(Boolean, index=True)
    probability = Column(Float)
    risk_level = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
