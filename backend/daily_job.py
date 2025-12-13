from fastapi import FastAPI, HTTPException

app = FastAPI()

# --- placeholder implementations ---
def fetch_and_save_cost_by_service(days: int):
    return [{"service": "EC2", "cost": 100}, {"service": "S3", "cost": 50}]

def detect_spike():
    return {"spike_detected": False}

def send_alert_if_needed():
    return {"alert_sent": True}

def generate_recommendations():
    return {"recommendations": ["Use reserved instances", "Optimize storage"]}

# --- endpoints ---
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
    try:
        return generate_recommendations()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))