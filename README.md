# 🛡️ FraudShield AI: Healthcare Claims Fraud Detection

FraudShield AI is a production-grade, full-stack machine learning application designed to identify and analyze fraudulent healthcare claims. Built with a SaaS-first mindset, it features a robust FastAPI backend, a high-performance XGBoost model, and a modern Streamlit dashboard for real-time intelligence.

## 🚀 Key Features

- **Advanced ML Pipeline**: XGBoost classifier integrated into a scikit-learn pipeline for high-precision fraud detection.
- **Model Explainability**: Deep insights into AI decisions using **SHAP** values, explaining *why* a claim was flagged.
- **Enterprise Security**: API Key authentication, rate limiting, and secure documentation endpoints.
- **Modern Dashboard**: SaaS-style UI with real-time KPI cards, financial impact analysis, and trend tracking.
- **Modular Architecture**: Strict separation of concerns (API, Services, ML Inference, Data Repository).
- **Full Observability**: Structured JSON logging and performance profiling for production monitoring.
- **Containerized**: Ready for deployment with Docker and Docker Compose.

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy (SQLite/PostgreSQL)
- **Frontend**: Streamlit, Plotly
- **Machine Learning**: XGBoost, Scikit-learn, SHAP
- **DevOps**: Docker, Pytest, Python-JSON-Logger

## 📦 Project Structure

```text
app/
├── api/          # FastAPI routes and dependencies
├── core/         # Configuration and settings
├── db/           # Models and Repository pattern
├── ml/           # Singleton model manager and inference
├── services/     # Business logic
├── utils/        # Middleware and loggers
└── dashboard.py  # Streamlit UI
models/           # Versioned ML models (.pkl)
scripts/          # Migration, seeding, and training scripts
tests/            # Unit and integration tests
```

## 🚥 Getting Started

### 1. Prerequisites
- Python 3.13+
- Docker (Optional)

### 2. Installation
```bash
# Clone the repository
git clone <repo-url>
cd FraudDetectionApp-main

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup
```bash
# Initialize and seed the database
python3 scripts/init_db.py
python3 scripts/seed_db.py

# (Optional) Retrain the model
python3 scripts/retrain_model.py
```

### 4. Running the Application
**Option A: Manual Start**
```bash
./run.sh
```

**Option B: Docker Compose**
```bash
docker-compose up --build
```

Access the dashboard at [http://localhost:8501](http://localhost:8501) and API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## 🧪 Testing
Run the test suite with coverage:
```bash
pytest --cov=app tests/
```

## 🔒 Security
- **API Authentication**: All backend requests require the `X-API-KEY` header.
- **Dashboard Login**: Default credentials: `admin` / `password123`.

---
*Developed for production-grade healthcare auditing.*
