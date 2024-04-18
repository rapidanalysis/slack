"""A simple Slack response"""

from slack_bolt import Say

def greetings(say: Say, command: dict):
    """Respond to the user, tagging them

    Args:
        say (Say): Sends a message to incomming command's channel
        command (dict): the message payload
    """
    say(f"Hey there <@{command['user_id']}>!")
