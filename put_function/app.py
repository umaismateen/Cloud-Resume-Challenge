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
        response = table.update_item(
            Key={
                'ID': 'visitors'
            },
            UpdateExpression='ADD visitors :inc',
            ExpressionAttributeValues={
                ':inc': 1
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps('Update successful')
        }

    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error updating item')
        }
    