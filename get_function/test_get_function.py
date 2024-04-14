import json
import boto3
import pytest
from moto import mock_aws
from get_function import app

@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    boto3.setup_default_session(aws_access_key_id="test", aws_secret_access_key="test", aws_session_token="test")

@pytest.fixture(scope='function')
def dynamodb(aws_credentials):
    with mock_aws():
        yield boto3.resource('dynamodb', region_name='us-east-1')

@pytest.fixture(scope='function')
def create_visitors_table(dynamodb):
    table = dynamodb.create_table(
        TableName='cloud-resume-challenge',
        KeySchema=[{'AttributeName': 'ID', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'ID', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )
    table.wait_until_exists()
    return table

def test_visitors_retrieved_successfully(create_visitors_table):
    create_visitors_table.put_item(Item={'ID': 'visitors', 'visitors': 123})
    
    response = app.lambda_handler({}, {})  # Mock event with ID
    body = json.loads(response['body'])

    assert response['statusCode'] == 200
    assert body['visitors'] == 123

def test_visitors_data_not_found(create_visitors_table):
    response = app.lambda_handler({}, {})  # Mock event with ID
    assert response['statusCode'] == 404
    assert json.loads(response['body']) == 'Visitors data not found'
