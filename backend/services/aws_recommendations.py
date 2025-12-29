import boto3
import os
from dotenv import load_dotenv

load_dotenv()
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

ec2 = boto3.client("ec2", region_name=AWS_REGION)

def get_ec2_recommendations():
    response = ec2.describe_instances()
    data = []

    for reservation in response["Reservations"]:
        for inst in reservation["Instances"]:
            data.append({
                "instance_id": inst["InstanceId"],
                "instance_type": inst["InstanceType"],
                "state": inst["State"]["Name"],
                "recommendation": "Review usage and downsize or stop if underutilized"
            })

    return data
