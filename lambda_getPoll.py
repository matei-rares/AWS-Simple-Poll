import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pollTable')

def lambda_handler(event, context):
    print(event)
    print(context)
    pid = event.get('params', {}).get('querystring', {}).get('id')
    print(pid)
    if not pid:
        return {
            "statusCode": 400,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": "Missing pid"
        }

    try:
        pid = int(pid)
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

    return {
        "statusCode": 200,
        "headers": { "Access-Control-Allow-Origin": "*" },
        "body": json.dumps({
            "question": item['question'],
            "options": list(item['options'].keys()),
            "ips": item['ips']
        })
    }

