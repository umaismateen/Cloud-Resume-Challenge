import json
import boto3
import pytest
from moto import mock_aws 
from put_function import app


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    boto3.setup_default_session(aws_access_key_id="test", aws_secret_access_key="test", aws_session_token="test")

@pytest.fixture(scope='function')
def dynamodb(aws_credentials):
    with mock_aws():  # Using mock_aws here
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
    # Pre-populate the table with an item to update
    table.put_item(Item={'ID': 'visitors', 'visitors': 123})
    return table

def test_update_visitors_successfully(create_visitors_table):
    response = app.lambda_handler({}, {})  # Mock event and context
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == 'Update successful'
    # Verify the item was updated
    updated_item = create_visitors_table.get_item(Key={'ID': 'visitors'})
    assert int(updated_item['Item']['visitors']) == 124  # Assuming initial count was 123
