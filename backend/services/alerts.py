# backend/services/alerts.py
import os
import requests
from dotenv import load_dotenv
from models.cost_model import daily
from services.recommendations import get_recommendations

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("BREVO_RECIPIENT_EMAIL")

BASE_URL = "https://api.brevo.com/v3/smtp/email"


def compute_7day_avg():
    docs = list(daily.find().sort("date_utc", -1).limit(8))
    if len(docs) < 2:
        return None

    values = [d["amount"] for d in docs[1:]]
    if not values:
        return None

    return sum(values) / len(values)


def detect_spike(threshold_pct=30.0):
    latest = daily.find_one(sort=[("date_utc", -1)])
    if not latest:
        return None

    avg7 = compute_7day_avg()
    if avg7 is None:
        return None

    increase = ((latest["amount"] - avg7) / avg7) * 100

    return {
        "is_spike": increase >= threshold_pct,
        "latest": latest["amount"],
        "avg7": round(avg7, 4),
        "increase_pct": round(increase, 2)
    }


def send_brevo_email(subject, html):
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "sender": {"email": SENDER_EMAIL},
        "to": [{"email": RECIPIENT_EMAIL}],
        "subject": subject,
        "htmlContent": html
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)
    return response.json()


def send_alert_if_needed():
    spike = detect_spike()
    recommendations = get_recommendations()

    if spike and spike["is_spike"]:
        html = f"""
        <h2>AWS Cost Spike Detected</h2>
        <p><b>Latest:</b> ${spike['latest']}</p>
        <p><b>7-day Avg:</b> ${spike['avg7']}</p>
        <p><b>Increase:</b> {spike['increase_pct']}%</p>

        <h3>Recommendations</h3>
        <pre>{recommendations}</pre>
        """

        return send_brevo_email(
            subject="AWS COST ALERT",
            html=html
        )

    return {"message": "No cost spike detected"}
