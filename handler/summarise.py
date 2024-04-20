"""Summarises text received from the user"""

import os

from slack_bolt import Ack, Say

from api.rapidanalysis import api_call

def summarise(say: Say, command: dict, ack: Ack):
    """Responds to the user with a summary of the text provided

    By default returns text equal to ~20% of the length of the original
    text provided by the user.

    Args:
        say (Say): Sends a message to incomming command's channel
        command (dict): the message payload
    """
    if command['text'] is None:
        ack()

    body = {
        'fulltext': command['text'],
        'percent': 0.2,
    }

    summary = api_call(
        api_method  = 'text/to-summary',
        data        = body,
        token       = os.getenv('RAPID_API_KEY')
    )

    say(f"Your summary <@{command['user_id']}>:\n{summary}")
