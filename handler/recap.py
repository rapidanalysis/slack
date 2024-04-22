"""Recaps the text received from the user"""

import os
import re

from slack_bolt import Respond
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from api.rapidanalysis import api_call

def recap(command: dict, respond: Respond, client: WebClient):
    """Responds to the user with a summary of the text provided

    By default returns text equal to ~20% of the length of the original
    text provided by the user.

    Args:
        say (Say): Sends a message to incomming command's channel
        command (dict): the message payload
    """
    print(command)
    msgs: list = _get_message_history(command['channel_id'], client)

    usernames = {}

    for member in client.users_list().get('members'):
        usernames[member['id']] = member['real_name']

    body = {
        'percent': 0.2,
        'fulltext': ''.join(map(
            lambda msg: usernames[msg['user_id']] + "\n" + msg['text'],
            msgs
        )),
    }

    summary = api_call(
        api_method  = 'text/to-summary',
        data        = body,
        token       = os.getenv('RAPID_API_KEY')
    )

    respond(f"Your summary <@{command['user_id']}>:\n{summary}")

def _get_message_history(channel_id: str, client: WebClient):
    """Gets Slack channel history from the past 90 days

    Args:
        command (dict): the command payload
    """

    channel_history: list = []

    try:
        result = client.conversations_history(channel=channel_id)

        channel_history = result["messages"]
    except SlackApiError as e:
        print(f"Error creating conversation: {e}")

    return channel_history

