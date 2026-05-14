import pytest

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "2.0.0"}

def test_unauthorized_access(client):
    response = client.get("/api/v1/history/")
    assert response.status_code == 403

def test_prediction_endpoint(client, auth_headers):
    payload = {
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
    response = client.post("/api/v1/predict/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "is_fraud" in data
    assert "probability" in data
    assert "risk_level" in data

def test_history_endpoint(client, auth_headers):
    response = client.get("/api/v1/history/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
