"""Summarises text received from the user"""

import os
from urllib.parse import ParseResult, urlparse, urlunparse

from slack_bolt import Ack, Respond
import urllib3

from api.rapidanalysis import api_call

def summarise(respond: Respond, command: dict, ack: Ack):
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

    # check for pastebin link
    parsed: ParseResult = urlparse(url=command['text'])
    if parsed.hostname == 'pastebin.com':
        http = urllib3.PoolManager()

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        raw_path: str = urlunparse(parsed._replace(path='raw' + parsed.path))

        res: urllib3.HTTPResponse = http.request('GET', raw_path,
                                                    headers = headers)

        body['fulltext'] = res.data.decode('utf-8')

    summary = api_call(
        api_method  = 'text/to-summary',
        data        = body,
        token       = os.getenv('RAPID_API_KEY')
    )

    respond(f"Your summary <@{command['user_id']}>:\n{summary}")
