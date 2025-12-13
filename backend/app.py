from services.recommendations import get_recommendations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.cost_service import fetch_today_cost, fetch_cost_by_service
from models.cost_model import save_cost_record
from services.cost_service import fetch_and_save_cost_by_service
from services.alerts import detect_spike, send_alert_if_needed

app = FastAPI(title="Cloud Cost Optimizer - Backend")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def root():
 return {"message": "FastAPI is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cost/today")
def cost_today():
    try:
        return fetch_today_cost()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cost/services")
def cost_services():
    try:
        return fetch_cost_by_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cost/save-today")
def save_today_cost():
    try:
        data = fetch_today_cost()
        amount = float(
            data["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
        )
        save_cost_record(amount)
        return {"saved": True, "amount": amount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cost/services/save")
def save_services():
    try:
        items = fetch_and_save_cost_by_service(days=30)
        return {"saved": True, "count": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts/check")
def check_spike():
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

@app.get("/recommendations")
def recommendations():
    return get_recommendations()