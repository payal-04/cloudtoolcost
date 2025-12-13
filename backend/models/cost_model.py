import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "cloudcost")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
daily = db.daily_cost

def save_cost_record(amount):
    doc = {
        "date_utc": datetime.utcnow(),
        "amount": float(amount)
    }
    daily.insert_one(doc)
    return True

def save_service_costs(items):
    for it in items:
        doc = {
            "service": it["service"],
            "amount": it["amount"],
            "period_start": it["period_start"],
            "saved_at": datetime.utcnow()
        }
        db.service_costs.insert_one(doc)
    return True 