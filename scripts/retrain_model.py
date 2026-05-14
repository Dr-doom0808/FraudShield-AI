import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import os
from datetime import datetime

# Paths to the new database
db_path = "/Users/shloksingh/Downloads/fraud detection ml database"
models_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")

def train_model():
    print("Loading data...")
    train_labels = pd.read_csv(os.path.join(db_path, "Train-1542865627584.csv"))
    beneficiary = pd.read_csv(os.path.join(db_path, "Train_Beneficiarydata-1542865627584.csv"))
    inpatient = pd.read_csv(os.path.join(db_path, "Train_Inpatientdata-1542865627584.csv"))
    outpatient = pd.read_csv(os.path.join(db_path, "Train_Outpatientdata-1542865627584.csv"))

    print("Merging data...")
    # Merge inpatient and outpatient
    claims = pd.concat([inpatient, outpatient], ignore_index=True)
    
    # Merge with beneficiary data
    df = pd.merge(claims, beneficiary, on='BeneID', how='inner')
    
    # Merge with labels
    df = pd.merge(df, train_labels, on='Provider', how='inner')

    print("Preprocessing...")
    # Map PotentialFraud to numeric
    df['PotentialFraud'] = df['PotentialFraud'].map({'Yes': 1, 'No': 0})

    # Preprocess Provider (strip 'PRV' and convert to int)
    df['Provider_Numeric'] = df['Provider'].apply(lambda x: int(x[3:]) if isinstance(x, str) and x.startswith('PRV') else 0)

    # Preprocess Chronic Conditions (CSV: 1=Yes, 2=No -> Model: 1=Yes, 0=No)
    chronic_cols = [
        'ChronicCond_Alzheimer', 'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
        'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression', 
        'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis', 
        'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke'
    ]
    for col in chronic_cols:
        df[col] = df[col].apply(lambda x: 1 if x == 1 else 0)

    # RenalDiseaseIndicator (CSV: "0" or "1" -> Model: 0 or 1)
    df['RenalDiseaseIndicator'] = df['RenalDiseaseIndicator'].apply(lambda x: 1 if str(x) == '1' or str(x) == 'Y' else 0)

    # Calculate TotalReimbursement
    df['TotalReimbursement'] = df['IPAnnualReimbursementAmt'] + df['OPAnnualReimbursementAmt']

    # Select top features
    top_features = [
        'Provider_Numeric', 'InscClaimAmtReimbursed', 'IPAnnualReimbursementAmt',
        'IPAnnualDeductibleAmt', 'TotalReimbursement', 'RenalDiseaseIndicator',
        'ChronicCond_Alzheimer', 'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
        'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression', 
        'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis', 
        'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke'
    ]
    
    # Ensure all columns exist and handle missing values
    for col in top_features:
        if col not in df.columns:
            df[col] = 0
    df = df.dropna(subset=['PotentialFraud'])
    df[top_features] = df[top_features].fillna(0)

    X = df[top_features]
    y = df['PotentialFraud']

    print(f"Training on {len(X)} records...")
    
    # Create Pipeline
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('classifier', xgb.XGBClassifier(
            learning_rate=0.1,
            max_depth=6,
            n_estimators=100,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss'
        ))
    ])
    
    pipeline.fit(X, y)
    
    # Model versioning with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = f"fraud_detection_model_{timestamp}.pkl"
    latest_model_name = "fraud_detection_model.pkl"
    
    print("Saving model versions...")
    # Save versioned model
    joblib.dump(pipeline, os.path.join(models_dir, model_name))
    # Save as latest
    joblib.dump(pipeline, os.path.join(models_dir, latest_model_name))
    
    print(f"Model saved: {model_name} and {latest_model_name}")

if __name__ == "__main__":
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    train_model()
