"""Register event listeners to the Slack handler"""

from slack_bolt import App, Ack

from .greetings import greetings
from .question import question
from .recap import recap
from .summarise import summarise

def respond_to_slack(ack: Ack):
    """Responds to slack within 3 seconds.

    Args:
        ack (Ack): Function to acknowledge incoming event.
    """
    ack()

def register_listeners(app: App):
    """Register listeners to app

    AWS Lambda sometimes terminates after returning a HTTP response, so
    uses lazy listeners to acknowledge after listener function is
    complete. Still requires listener method to finish within 3 seconds.

    Args:
        app (App): the Slack App
    """
    app.command("/greetings")(
        ack = respond_to_slack,
        lazy = [greetings]
    )
  
    app.command("/question")(
        ack = respond_to_slack,
        lazy = [question]
    )
    
    app.command("/recap")(
        ack = respond_to_slack,
        lazy = [recap]
    )

    app.command("/summarise")(
        ack = respond_to_slack,
        lazy = [summarise]
    )
