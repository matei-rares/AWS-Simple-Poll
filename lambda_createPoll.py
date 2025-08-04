import json
import boto3
import random
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pollTable')

def lambda_handler(event, context):
    question = event.get('question')
    options = event.get('options')

    if not question or not options or not isinstance(options, list):
        return {
            "statusCode": 400,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": "Invalid input"
        }

    pid = random.randint(100000, 999999)
    
    options_map = { opt: 0 for opt in options }
    print (options_map)
    item = {
        'PID': pid,
        'question': question,
        'options': options_map,
        'ips':[]
    }

    table.put_item(Item=item)
    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*" },
        "body": json.dumps({ "PID": pid })
    }
