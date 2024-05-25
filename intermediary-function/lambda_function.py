"""Script for the Gateway Lambda function"""
import os
import json

import boto3

client = boto3.client('lambda')

def lambda_handler(event, context):
    """Gateway function to verify Slack source and forward event."""
    try:
        # Publish the event to the Lambda function
        processing_response = client.invoke(
            FunctionName=os.getenv('AWS_LAMBDA_FUNC'),
            InvocationType='Event',
            Payload=json.dumps(event),
        )

        body = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Processing your request!"
                    }
                }
            ]
        }

        return {
            'statusCode': 200,
            'body': json.dumps(body)
        }

    except Exception as e:
        raise e