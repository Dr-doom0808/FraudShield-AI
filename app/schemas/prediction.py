from pydantic import BaseModel
from typing import Dict, Any, Optional

class PredictionResult(BaseModel):
    is_fraud: bool
    probability: float
    risk_level: str
    explanation: Optional[Dict[str, float]] = None
