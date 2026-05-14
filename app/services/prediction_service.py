import pandas as pd
import joblib
import shap
from app import schemas
from app.db.models import Claim, Prediction
from sqlalchemy.orm import Session
from typing import Optional
from app.utils.logger import logger
import numpy as np

def _load_model(model_path: str):
    try:
        return joblib.load(model_path)
    except Exception as e:
        logger.error(f"Failed to load model from {model_path}: {e}")
        raise

def _detect_drift(df_scaled: np.ndarray):
    """
    Mock data drift detection.
    In a real-world app, this would compare current data distribution with training distribution.
    """
    # Simple check: are values within expected ranges?
    # This is a placeholder for a more complex implementation (e.g., using EvidentlyAI or custom statistical tests)
    mean_val = np.mean(df_scaled)
    if abs(mean_val) > 3.0: # 3 standard deviations away from mean (0 for scaled data)
        logger.warning(f"Data Drift Detected: Current batch mean {mean_val:.2f} is unusually high!")
        return True
    return False

def _predict_fraud(model, claim_data: schemas.Claim, explain: bool = False):
    # Convert claim data to DataFrame
    df = pd.DataFrame([claim_data.dict()])
    
    logger.info(f"Predicting for provider: {claim_data.Provider}")

    # Preprocess Provider
    df['Provider_Numeric'] = df['Provider'].apply(lambda x: int(x[3:]) if isinstance(x, str) and x.startswith('PRV') else 0)

    # Select top features (must match the order used during training)
    top_features = [
        'Provider_Numeric', 'InscClaimAmtReimbursed', 'IPAnnualReimbursementAmt',
        'IPAnnualDeductibleAmt', 'TotalReimbursement', 'RenalDiseaseIndicator',
        'ChronicCond_Alzheimer', 'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
        'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression', 
        'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis', 
        'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke'
    ]
    df = df[top_features]

    # Predict using pipeline
    classifier = model.named_steps['classifier']
    scaler = model.named_steps['scaler']
    
    df_scaled = scaler.transform(df)
    
    # Check for drift
    _detect_drift(df_scaled)

    prediction = classifier.predict(df_scaled)
    probability = classifier.predict_proba(df_scaled)[:, 1]

    is_fraud = bool(prediction[0])
    prob = float(probability[0])

    if prob > 0.75:
        risk_level = "High"
    elif prob > 0.5:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    logger.info(f"Prediction for {claim_data.Provider}: Result={is_fraud}, Probability={prob:.4f}, Risk={risk_level}")

    explanation = None
    if explain:
        logger.info(f"Generating SHAP explanation for {claim_data.Provider}")
        # Explain using TreeExplainer (works for XGBoost)
        explainer = shap.TreeExplainer(classifier)
        shap_values = explainer.shap_values(df_scaled)
        
        # Convert shap values to a dict of feature names and values
        # shap_values is an array for binary classification
        if isinstance(shap_values, list): # For some versions of SHAP
            shap_vals = shap_values[1][0]
        else:
            shap_vals = shap_values[0]
            
        explanation = dict(zip(top_features, [float(v) for v in shap_vals]))

    return schemas.PredictionResult(
        is_fraud=is_fraud, 
        probability=prob, 
        risk_level=risk_level,
        explanation=explanation
    )

def predict(model_path: str, claim_data: schemas.Claim, db: Session, explain: bool = False):
    model = _load_model(model_path)
    result = _predict_fraud(model, claim_data, explain=explain)

    # Save claim and prediction to database
    db_claim = Claim(**claim_data.dict())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)

    db_prediction = Prediction(claim_id=db_claim.id, **result.dict(exclude={'explanation'}))
    db.add(db_prediction)
    db.commit()

    return result

def batch_predict(model_path: str, claims_data: list[schemas.Claim], db: Session):
    model = _load_model(model_path)
    results = []
    for claim_data in claims_data:
        result = _predict_fraud(model, claim_data, explain=False) # Batch usually doesn't need SHAP
        results.append(result)

        # Save to database
        db_claim = Claim(**claim_data.dict())
        db.add(db_claim)
        db.commit()
        db.refresh(db_claim)

        db_prediction = Prediction(claim_id=db_claim.id, **result.dict(exclude={'explanation'}))
        db.add(db_prediction)
        db.commit()

    return results
