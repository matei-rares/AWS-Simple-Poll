
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pollTable')

def lambda_handler(event, context):
    pid_str = event.get('params', {}).get('querystring', {}).get('id')
    
    if not pid_str:
        return {
            "statusCode": 400,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": "Missing pid"
        }

    try:
        pid = int(pid_str)
    except ValueError:
        return {
            "statusCode": 400,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": "Invalid pid"
        }

    response = table.get_item(Key={'PID': pid})
    item = response.get('Item')

    if not item:
        return {
            "statusCode": 404,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": "Poll not found"
        }

    options = { k: str(v) for k, v in item['options'].items() }


    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*" },
        "body": json.dumps(options)
    }