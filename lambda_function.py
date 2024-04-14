"""A lambda handler for Slack events"""

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

app = App(process_before_response=True)

def lambda_handler(event, context):
    handler = SlackRequestHandler(app = app)
    return handler.handle(event, context)
