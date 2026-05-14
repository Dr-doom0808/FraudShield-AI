import sys
import os
import pandas as pd
from sqlalchemy.orm import Session

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine
from app.db.models import Claim, Base

# Paths to the CSV database
db_path = "/Users/shloksingh/Downloads/fraud detection ml database"

def seed_data(limit=100):
    print(f"Seeding {limit} records from CSVs into SQLite database...")
    
    # Initialize DB tables
    Base.metadata.create_all(bind=engine)
    
    # Load raw data
    try:
        beneficiary = pd.read_csv(os.path.join(db_path, "Train_Beneficiarydata-1542865627584.csv")).head(limit)
        inpatient = pd.read_csv(os.path.join(db_path, "Train_Inpatientdata-1542865627584.csv")).head(limit)
        
        # Merge basic info
        df = pd.merge(inpatient, beneficiary, on='BeneID', how='inner')
        
        # Calculate TotalReimbursement
        df['TotalReimbursement'] = df['IPAnnualReimbursementAmt'] + df['OPAnnualReimbursementAmt']
        
        # Map chronic conditions (CSV: 1=Yes, 2=No -> DB: 1=Yes, 0=No)
        chronic_cols = [
            'ChronicCond_Alzheimer', 'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
            'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression', 
            'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis', 
            'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke'
        ]
        for col in chronic_cols:
            df[col] = df[col].apply(lambda x: 1 if x == 1 else 0)
            
        # RenalDiseaseIndicator
        df['RenalDiseaseIndicator'] = df['RenalDiseaseIndicator'].apply(lambda x: 1 if str(x) == '1' or str(x) == 'Y' else 0)

        db = SessionLocal()
        
        # Clear existing claims
        db.query(Claim).delete()
        
        for _, row in df.iterrows():
            claim = Claim(
                Provider=row['Provider'],
                InscClaimAmtReimbursed=float(row['InscClaimAmtReimbursed']),
                IPAnnualReimbursementAmt=float(row['IPAnnualReimbursementAmt']),
                IPAnnualDeductibleAmt=float(row['IPAnnualDeductibleAmt']),
                TotalReimbursement=float(row['TotalReimbursement']),
                RenalDiseaseIndicator=int(row['RenalDiseaseIndicator']),
                ChronicCond_Alzheimer=int(row['ChronicCond_Alzheimer']),
                ChronicCond_Heartfailure=int(row['ChronicCond_Heartfailure']),
                ChronicCond_KidneyDisease=int(row['ChronicCond_KidneyDisease']),
                ChronicCond_Cancer=int(row['ChronicCond_Cancer']),
                ChronicCond_ObstrPulmonary=int(row['ChronicCond_ObstrPulmonary']),
                ChronicCond_Depression=int(row['ChronicCond_Depression']),
                ChronicCond_Diabetes=int(row['ChronicCond_Diabetes']),
                ChronicCond_IschemicHeart=int(row['ChronicCond_IschemicHeart']),
                ChronicCond_Osteoporasis=int(row['ChronicCond_Osteoporasis']),
                ChronicCond_rheumatoidarthritis=int(row['ChronicCond_rheumatoidarthritis']),
                ChronicCond_stroke=int(row['ChronicCond_stroke'])
            )
            db.add(claim)
        
        db.commit()
        db.close()
        print(f"Successfully seeded {len(df)} records!")
        
    except Exception as e:
        print(f"Error during seeding: {e}")

if __name__ == "__main__":
    seed_data()
