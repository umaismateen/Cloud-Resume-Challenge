import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Initialize a DynamoDB client with Boto3
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # Reference the DynamoDB table
    table = dynamodb.Table('cloud-resume-challenge')    

    # Update the item in the table
    try:
        response = table.get_item(
            Key={
                'ID': 'visitors'
            },
        )       
        if 'Item' in response:
            visitors = response['Item'].get('visitors', 0)
            return {
                'statusCode': 200,
                'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET',
                },
                'body': json.dumps({'visitors': int(visitors)})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Visitors data not found')
            }

    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving item')
        }
    