import pytest
import pandas as pd
from app.ml.inference import model_manager
from app import schemas

def test_model_manager_singleton():
    mm1 = model_manager
    from app.ml.inference import ModelManager
    mm2 = ModelManager()
    assert mm1 is mm2

def test_inference_logic():
    # Create a dummy claim
    claim = {
        "Provider": "PRV51001",
        "InscClaimAmtReimbursed": 1000.0,
        "IPAnnualReimbursementAmt": 5000.0,
        "IPAnnualDeductibleAmt": 1000.0,
        "TotalReimbursement": 6000.0,
        "RenalDiseaseIndicator": 0,
        "ChronicCond_Alzheimer": 0,
        "ChronicCond_Heartfailure": 0,
        "ChronicCond_KidneyDisease": 0,
        "ChronicCond_Cancer": 0,
        "ChronicCond_ObstrPulmonary": 0,
        "ChronicCond_Depression": 0,
        "ChronicCond_Diabetes": 0,
        "ChronicCond_IschemicHeart": 0,
        "ChronicCond_Osteoporasis": 0,
        "ChronicCond_rheumatoidarthritis": 0,
        "ChronicCond_stroke": 0
    }
    df = pd.DataFrame([claim])
    # Preprocess provider like in the service
    df['Provider_Numeric'] = df['Provider'].apply(lambda x: int(x[3:]))
    features = [
        'Provider_Numeric', 'InscClaimAmtReimbursed', 'IPAnnualReimbursementAmt',
        'IPAnnualDeductibleAmt', 'TotalReimbursement', 'RenalDiseaseIndicator',
        'ChronicCond_Alzheimer', 'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
        'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression', 
        'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis', 
        'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke'
    ]
    df = df[features]
    
    prediction, probability = model_manager.predict(df)
    assert len(prediction) == 1
    assert 0 <= probability[0] <= 1
