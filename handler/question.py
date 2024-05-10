"""Recaps the text received from the user"""

import os
import re

from slack_bolt import Respond
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from api.rapidanalysis import api_call

def question(command: dict, respond: Respond, client: WebClient):
    """Responds to the user with a response to the given prompt

    Args:
        say (Say): Sends a message to incomming command's channel
        command (dict): the message payload
    """
    if command['text'] is None:
        respond("Usage: /recap *prompt*")
        return

    msgs: list = _get_message_history(command['channel_id'], client)

    usernames = {}

    for member in client.users_list().get('members'):
        if 'real_name' in member:
            usernames[member['id']] = member['real_name']
        else:
            # Account is most likely deactivated so just use the name
            usernames[member['id']] = member['name']

    body = {
        'prompt': command['text'],
        'text': ''.join(map(
            lambda msg: _format_message(msg, usernames),
            reversed(msgs) # supply messages from oldest to newest
        )),
    }

    summary = api_call(
        api_method  = 'generate/text-from-text',
        data        = body,
        token       = os.getenv('RAPID_API_KEY')
    )

    respond(f"Your summary <@{command['user_id']}>:\n{summary}")

def _get_message_history(channel_id: str, client: WebClient):
    """Gets Slack channel history from the last 100 messages

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

def _format_message(msg: dict, usernames: dict):
    """Prepend messager name, and convert mentions

    Prepends the message text with the messager, and convert all
    mentions (<@user_id>, with user_id starting with U or W) to be the
    user's name.

    Args:
        msg (dict): The message payload.
        usernames (dict): A map for user id's to name.
    """

    # convert all mentions to names <@user_id> -> name
    msg_mentions = re.sub(
        r"<@((U|W)[A-z0-9]+)>",
        lambda match: usernames[match.group(1)],
        msg['text']
    )

    return usernames[msg['user']] + "\n" + msg_mentions
