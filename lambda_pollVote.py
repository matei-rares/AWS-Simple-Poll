import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pollTable')

def lambda_handler(event, context):
    print(event)
    pid = int(event.get('body-json', {}).get('pollId'))
    print(pid)
    
    option = event.get('body-json', {}).get('option')
    ip = str(event.get('body-json',{}).get('visitorId'))

    try:
        item = table.get_item(Key={'PID': pid}).get('Item')
        
        if not item:
            return {
                "statusCode": 404,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": "Poll not found"
            }

        if 'ips' in item and ip in item['ips']:
            return {
                "statusCode": 403,
                "headers": { "Access-Control-Allow-Origin": "*" },
                "body": "This fingerprint has already voted."
            }

       

        response = table.update_item(
            Key={'PID': pid},
            UpdateExpression="""
                SET options.#opt = if_not_exists(options.#opt, :zero) + :inc,
                    ips = list_append(if_not_exists(ips, :empty_list), :new_ip)
            """,
            ExpressionAttributeNames={
                '#opt': option
            },
            ExpressionAttributeValues={
                ':inc': 1,
                ':zero': 0,
                ':new_ip': [ip],
                ':empty_list': []
            },
            ReturnValues="UPDATED_NEW"
        )

        return {
            "statusCode": 200,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": json.dumps({ "newCount": str(response['Attributes']['options'][option]) })
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "headers": { "Access-Control-Allow-Origin": "*" },
            "body": f"Error updating vote: {str(e)}"
        }
