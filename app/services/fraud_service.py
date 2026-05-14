import pandas as pd
from sqlalchemy.orm import Session
from app import schemas
from app.ml.inference import model_manager
from app.db.repository import fraud_repo
from app.utils.logger import logger

def process_prediction(db: Session, claim_data: schemas.Claim, explain: bool = False):
    """
    Business logic for single prediction:
    1. Preprocess data
    2. Run ML inference
    3. Persist claim and prediction
    4. Generate explanation if requested
    """
    # Preprocessing
    df = pd.DataFrame([claim_data.dict()])
    df['Provider_Numeric'] = df['Provider'].apply(
        lambda x: int(x[3:]) if isinstance(x, str) and x.startswith('PRV') else 0
    )
    
    # Feature ordering (must match training)
    features = [
        'Provider_Numeric', 'InscClaimAmtReimbursed', 'IPAnnualReimbursementAmt',
        'IPAnnualDeductibleAmt', 'TotalReimbursement', 'RenalDiseaseIndicator',
        'ChronicCond_Alzheimer', 'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
        'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression', 
        'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis', 
        'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke'
    ]
    df = df[features]
    
    # ML Inference
    prediction, probability = model_manager.predict(df)
    is_fraud = bool(prediction[0])
    prob = float(probability[0])
    
    # Risk Level logic
    risk_level = "High" if prob > 0.75 else "Medium" if prob > 0.5 else "Low"
    
    # Explanation logic
    explanation = None
    if explain:
        explanation_values = model_manager.explain(df)
        explanation = dict(zip(features, [float(v) for v in explanation_values]))
    
    # Data Access logic
    db_claim = fraud_repo.create_claim(db, claim_data)
    prediction_entry = {
        "claim_id": db_claim.id,
        "is_fraud": is_fraud,
        "probability": prob,
        "risk_level": risk_level
    }
    fraud_repo.create_prediction(db, prediction_entry)
    
    logger.info(f"Processed prediction for provider {claim_data.Provider}: Result={is_fraud}")
    
    return schemas.PredictionResult(
        is_fraud=is_fraud,
        probability=prob,
        risk_level=risk_level,
        explanation=explanation
    )

def process_batch_prediction(db: Session, claims_data: list[schemas.Claim]):
    """
    Business logic for batch prediction.
    """
    results = []
    for claim in claims_data:
        # We reuse the logic but usually skip heavy SHAP in batch
        res = process_prediction(db, claim, explain=False)
        results.append(res)
    return results

def get_dashboard_stats(db: Session):
    return fraud_repo.get_stats(db)

def get_prediction_history(db: Session, limit: int = 100):
    history_data = fraud_repo.get_history(db, limit)
    return [
        {
            "id": p.id,
            "claim_id": c.id,
            "Provider": c.Provider,
            "is_fraud": p.is_fraud,
            "probability": p.probability,
            "risk_level": p.risk_level,
            "amount": c.InscClaimAmtReimbursed,
            "created_at": p.created_at.isoformat() if p.created_at else None
        } for p, c in history_data
    ]

def get_advanced_analytics(db: Session):
    """
    Get complex analytics for the dataset.
    """
    # Fetch all claims and predictions for analysis
    claims = fraud_repo.get_seeded_claims(db, limit=1000)
    predictions = db.query(fraud_repo.models.Prediction).all()
    
    if not claims or not predictions:
        return {}

    # Convert to DataFrames
    claims_df = pd.DataFrame([c.__dict__ for c in claims])
    preds_df = pd.DataFrame([p.__dict__ for p in predictions])
    
    # Basic analytics
    avg_prob = float(preds_df['probability'].mean())
    high_risk_count = int(preds_df[preds_df['risk_level'] == 'High'].shape[0])
    
    # Correlation (simplified for example)
    corr_features = ['InscClaimAmtReimbursed', 'IPAnnualReimbursementAmt', 'TotalReimbursement']
    correlation = claims_df[corr_features].corr().to_dict()
    
    # Distribution of risk levels
    risk_dist = preds_df['risk_level'].value_counts().to_dict()
    
    return {
        "avg_probability": avg_prob,
        "high_risk_count": high_risk_count,
        "correlation": correlation,
        "risk_distribution": risk_dist,
        "total_claims": len(claims),
        "total_predictions": len(predictions)
    }
