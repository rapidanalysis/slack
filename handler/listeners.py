"""Register event listeners to the Slack handler"""

from slack_bolt import App

from .greetings import greetings

def register_listeners(app: App):
    """Register listeners to app

    Args:
        app (App): the Slack App
    """
    app.command("/greetings")(greetings)
