import boto3
import json
from datetime import datetime

# AWS Setup
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CyberAttackLogs')

# Load Honeypot Logs
with open("/home/ubuntu/cowrie/var/log/cowrie/cowrie.json", "r") as file:
    logs = json.load(file)

for log in logs:
    table.put_item(
        Item={
            'attack_id': log['session'],
            'timestamp': log['timestamp'],
            'ip': log['src_ip'],
            'attack_type': log['eventid']
        }
    )
print("Logs uploaded to DynamoDB")
