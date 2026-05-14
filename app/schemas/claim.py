from pydantic import BaseModel, Field, validator

class Claim(BaseModel):
    Provider: str = Field(..., description="Provider code, e.g., PRV51001")
    InscClaimAmtReimbursed: float = Field(..., ge=0, description="Reimbursed claim amount")
    IPAnnualReimbursementAmt: float = Field(..., ge=0)
    IPAnnualDeductibleAmt: float = Field(..., ge=0)
    TotalReimbursement: float = Field(..., ge=0)
    RenalDiseaseIndicator: int = Field(..., ge=0, le=1)
    ChronicCond_Alzheimer: int = Field(..., ge=0, le=1)
    ChronicCond_Heartfailure: int = Field(..., ge=0, le=1)
    ChronicCond_KidneyDisease: int = Field(..., ge=0, le=1)
    ChronicCond_Cancer: int = Field(..., ge=0, le=1)
    ChronicCond_ObstrPulmonary: int = Field(..., ge=0, le=1)
    ChronicCond_Depression: int = Field(..., ge=0, le=1)
    ChronicCond_Diabetes: int = Field(..., ge=0, le=1)
    ChronicCond_IschemicHeart: int = Field(..., ge=0, le=1)
    ChronicCond_Osteoporasis: int = Field(..., ge=0, le=1)
    ChronicCond_rheumatoidarthritis: int = Field(..., ge=0, le=1)
    ChronicCond_stroke: int = Field(..., ge=0, le=1)

    @validator('Provider')
    def validate_provider(cls, v):
        if not v.startswith('PRV'):
            raise ValueError("Provider code must start with 'PRV'")
        return v

class ClaimInDB(Claim):
    id: int

    class Config:
        orm_mode = True
