# backend/services/alerts.py
import os
import requests
from datetime import timedelta
from dotenv import load_dotenv
from models.cost_model import daily
from services.recommendations import generate_recommendations

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("BREVO_RECIPIENT_EMAIL")

BASE_URL = "https://api.brevo.com/v3/smtp/email"


def compute_7day_avg():
    docs = list(daily.find().sort("date_utc", -1).limit(8))
    if len(docs) < 2:
        return None
    # exclude latest (docs[0]) so next 7 used for average
    vals = [d["amount"] for d in docs[1:]]
    if not vals:
        return None
    return sum(vals) / len(vals)


def detect_spike(threshold_pct=30.0):
    latest = daily.find_one(sort=[("date_utc", -1)])
    if not latest:
        return None
    latest_amt = latest["amount"]
    avg7 = compute_7day_avg()
    if avg7 is None:
        return None
    increase = ((latest_amt - avg7) / avg7) * 100.0
    is_spike = increase >= threshold_pct
    return {"is_spike": is_spike, "latest": latest_amt, "avg7": round(avg7, 4), "increase_pct": round(increase, 2)}


def send_brevo_email(subject: str, html_content: str):
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "sender": {"email": SENDER_EMAIL},
        "to": [{"email": RECIPIENT_EMAIL}],
        "subject": subject,
        "htmlContent": html_content,
    }
    response = requests.post(BASE_URL, json=payload, headers=headers)
    return response.json()


def send_alert_if_needed():
    spike = detect_spike()
    recs = generate_recommendations()
    if spike and spike["is_spike"]:
        subject = f"[ALERT] AWS Cost Spike: ${spike['latest']}"
        html = f"""
        <h2>AWS Cost Spike Detected!</h2>
        <p><b>Latest cost:</b> ${spike['latest']}</p>
        <p><b>7-day avg:</b> ${spike['avg7']}</p>
        <p><b>Increase:</b> {spike['increase_pct']}%</p>

        <h3>Recommendations</h3>
        <pre>{recs}</pre>
        """
        return send_brevo_email(subject, html)
    return {"skipped": True}
