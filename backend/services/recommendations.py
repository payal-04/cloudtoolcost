# backend/services/recommendations.py

from datetime import datetime

def get_recommendations():
    """
    Returns cloud cost optimization recommendations.
    This version is SAFE (no AWS API calls).
    """

    recommendations = {
        "generated_at": datetime.utcnow().isoformat(),

        "ec2_recommendations": [
            {
                "issue": "Idle or underutilized EC2 instances",
                "recommendation": (
                    "Identify EC2 instances with low CPU utilization "
                    "(<15% average) and consider stopping or downsizing them."
                ),
                "potential_saving": "Medium to High"
            },
            {
                "issue": "Over-provisioned instance types",
                "recommendation": (
                    "Use smaller instance types (e.g., t3.micro instead of t3.large) "
                    "for development or testing workloads."
                ),
                "potential_saving": "High"
            }
        ],

        "ebs_recommendations": [
            {
                "issue": "Unattached EBS volumes",
                "recommendation": (
                    "Delete EBS volumes that are not attached to any EC2 instance. "
                    "These volumes continue to incur cost even when unused."
                ),
                "potential_saving": "Medium"
            }
        ],

        "s3_recommendations": [
            {
                "issue": "Old objects stored in S3 Standard",
                "recommendation": (
                    "Move objects older than 30–90 days to S3 Glacier or "
                    "S3 Intelligent-Tiering using lifecycle policies."
                ),
                "potential_saving": "High"
            },
            {
                "issue": "Unused S3 buckets",
                "recommendation": (
                    "Delete empty or unused S3 buckets to reduce storage and request costs."
                ),
                "potential_saving": "Low to Medium"
            }
        ],

        "load_balancer_recommendations": [
            {
                "issue": "Idle Load Balancers",
                "recommendation": (
                    "Remove load balancers that receive little or no traffic "
                    "to avoid unnecessary hourly charges."
                ),
                "potential_saving": "Medium"
            }
        ]
    }

    return recommendations
