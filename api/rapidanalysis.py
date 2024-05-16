"""A Python module for interating with RapidAnalysis's API."""

import json
from typing import Final, Optional
from urllib.parse import urljoin
import urllib3

BASE_URL: Final[str] = 'https://api.weburban.com/'

http = urllib3.PoolManager()

def api_call(
    api_method: str,
    data: dict,
    token: str,
) -> Optional[dict]:
    """Sends an api request to RapidAnalysis returning its 'Output' value.

    Args:
        api_method (str): the api method to be used.
        payload (dict): The payload to be sent with the request.

    Returns:
        The 'output' object returned by RapidAnalysis or None if the
            request failed.
    """

    api_url = urljoin(BASE_URL, api_method)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': token,
    }

    encoded_data = json.dumps(data).encode('utf-8')

    res: urllib3.HTTPResponse = http.request('POST', api_url,
                                                 headers = headers,
                                                 body = encoded_data)

    body_json: dict = json.loads(res.data.decode('utf-8'))

    # Force dict to be case-insensitive
    body_json = {key.casefold(): val for key, val in body_json.items()}

    # check if request succeeded, and a vaild response received
    if (res.status != 200 or
        "output" not in body_json):
        return None

    return body_json["output"]
