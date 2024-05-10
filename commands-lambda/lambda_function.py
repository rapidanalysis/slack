"""A lambda handler for Slack events"""

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

from handler.listeners import register_listeners

app = App(process_before_response=True)

# register all listeners for slack
register_listeners(app)


def lambda_handler(event, context):
    handler = SlackRequestHandler(app = app)
    return handler.handle(event, context)
