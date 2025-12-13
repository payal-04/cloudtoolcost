# backend/services/recommendations.py
from .ec2_service import list_running_instances, suggest_rightsizing
from .ebs_service import list_unattached_volumes
from .elb_service import find_idle_load_balancers

def generate_recommendations():
    recs = {
        "ec2_rightsizing": [],
        "unattached_ebs": [],
        "idle_elbs": [],
        "s3": []
    }

    instances = list_running_instances()
    recs["ec2_rightsizing"] = suggest_rightsizing(instances, cpu_threshold=15.0)
    recs["unattached_ebs"] = list_unattached_volumes(days_unused=7)
    recs["idle_elbs"] = find_idle_load_balancers(request_threshold_per_day=10)
    recs["s3"] = [
        {"suggestion": "Consider enabling lifecycle rules to move aged objects to cheaper storage (Glacier/Intelligent-Tiering)."}
    ]
    return recs
