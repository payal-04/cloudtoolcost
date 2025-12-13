import boto3 
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from models.cost_model import save_service_costs


def fetch_and_save_cost_by_service(days=30):
    start, end = get_dates(days, 0)
    resp = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
    )
    groups = resp["ResultsByTime"][0]["Groups"]
    svc_list = []
    for g in groups:
        svc_list.append({
            "service": g["Keys"][0],
            "amount": float(g["Metrics"]["UnblendedCost"]["Amount"]),
            "period_start": start
        })
    save_service_costs(svc_list)
    return svc_list

# Load .env variables
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize AWS Cost Explorer client
ce = boto3.client(
    "ce",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def format_date(dt):
    return dt.strftime("%Y-%m-%d")

def get_dates(start_days, end_days):
    """
    start_days = how many days back to start
    end_days = how many days back to end
    """
    end = datetime.utcnow() - timedelta(days=end_days)
    start = datetime.utcnow() - timedelta(days=start_days)
    return format_date(start), format_date(end)

# =========================
# FETCH TODAY COST
# =========================
def fetch_today_cost():
    start, end = get_dates(1, 0)

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="DAILY",
            Metrics=["UnblendedCost"],
        )

        # Extract cost safely
        results = response.get("ResultsByTime", [])
        if not results:
            return {"amount": 0, "message": "No cost data available yet"}

        amount = float(results[0]["Total"]["UnblendedCost"]["Amount"])

        return {
            "start": start,
            "end": end,
            "amount": amount
        }

    except Exception as e:
        return {"error": str(e)}


# =========================
# FETCH COST GROUPED BY SERVICE
# =========================
def fetch_cost_by_service(days=30):
    start, end = get_dates(days, 0)

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={"Start": start, "End": end},
            Granularity="MONTHLY",
            Metrics=["UnblendedCost"],
            GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
        )

        services = []
        results = response.get("ResultsByTime", [])

        if results:
            for group in results[0].get("Groups", []):
                service_name = group["Keys"][0]
                cost_amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
                services.append({"service": service_name, "amount": cost_amount})

        return {
            "start": start,
            "end": end,
            "services": services
        }

    except Exception as e:
        return {"error": str(e)}
    
   