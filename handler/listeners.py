"""Register event listeners to the Slack handler"""

from slack_bolt import App

def register_listeners(app: App):
    """Register listeners to app

    Args:
        app (App): the Slack App
    """
