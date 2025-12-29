from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Cost services
from services.cost_service import fetch_and_save_cost_by_service

# Recommendations (Day 2 – safe version)
from services.recommendations import get_recommendations

# Alerts (Brevo)
from services.alerts import detect_spike, send_alert_if_needed

# Cost prediction (Day 3 – ML)
from services.cost_prediction import predict_next_7_days

# AWS recommendations (Day 3 – read-only)
from services.aws_recommendations import get_ec2_recommendations

app = FastAPI(title="Cloud Cost Optimization Tool")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- HEALTH --------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------- COST --------------------
@app.get("/cost/today")
def get_today_cost():
    try:
        # If you have a real service function, call it here
        # return fetch_today_cost()
        # For now, return mock data so frontend works
        return {
            "ResultsByTime": [
                {
                    "Total": {
                        "UnblendedCost": {
                            "Amount": "12.34",
                            "Unit": "USD"
                        }
                    }
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/cost/services")
def save_service_cost():
    try:
        return fetch_and_save_cost_by_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- RECOMMENDATIONS --------------------
@app.get("/recommendations")
def recommendations():
    try:
        # return get_recommendations()
        # Mock data for frontend
        return [
            "Stop unused EC2 instances",
            "Switch S3 buckets to Infrequent Access",
            "Use reserved instances for steady workloads"
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- ALERTS --------------------
@app.get("/alerts/check")
def check_alerts():
    try:
        return detect_spike()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerts/send")
def send_alert():
    try:
        return send_alert_if_needed()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- PREDICTION --------------------
@app.get("/cost/predictions")
def get_predictions():
    try:
        # return predict_next_7_days()
        # Mock data for frontend
        return [
            {"date": "2025-12-30", "amount": 12.34},
            {"date": "2025-12-31", "amount": 13.45},
            {"date": "2026-01-01", "amount": 14.10}
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- AWS (READ-ONLY) --------------------
@app.get("/aws/ec2-recommendations")
def aws_ec2_recommendations():
    return get_ec2_recommendations()

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"status": "Backend is running"}
