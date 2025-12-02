# Model Serving with REST API and Batch Inference

## Students
- **Student A:** Eric 'Hunter' Petross
- **Student B:** Samantha Pomeroy

## Setup Instructions
- Create and activate a Python 3.11 environment
- Install dependencies: `pip install -r requirements.txt`
- Train model (optional): `python -c "from models.train import train_and_save; train_and_save('models/baseline.joblib')"`

## Run Locally
- Start server: `uvicorn app.main:app --reload`
- Health: `curl http://localhost:8000/health`
- Predict: `curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"x1":1.0,"x2":2.0}'`
- Metrics: `curl http://localhost:8000/metrics`

## API Usage Examples
- GET `/health` → `{"status":"ok"}`
- POST `/predict` body `{"x1":1.5,"x2":2.3}` → `{"score":0.xx,"model_version":"v1.0"}`
- GET `/metrics` → Prometheus text exposition

## Batch Inference Usage
- Command: `python batch_infer.py data/input.csv data/predictions.csv`
- Input CSV columns: `x1,x2`
- Output CSV contains original columns plus `prediction`

## Docker Instructions
- Build: `docker build -t model-server:v1 .`
- Run: `docker run -p 8000:8000 model-server:v1`
- Test: `curl http://localhost:8000/health`

## Testing Checklist
- `uvicorn app.main:app --reload` starts
- `curl http://localhost:8000/health` returns 200
- `curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"x1":1.0,"x2":2.0}'` returns prediction
- `curl http://localhost:8000/metrics` shows metrics
- `python batch_infer.py data/input.csv data/predictions.csv` creates output
- Docker builds and runs; endpoints accessible on `http://localhost:8000`