import requests
import json
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_response(response: requests.models.Response):
    """Logs a HTTP response.

    Args:
        response (requests.models.Response): The HTTP response to log.
    """
    # Check if the response has a JSON body
    if response.headers.get("content-type") == "application/json":
        try:
            # Pretty-print the JSON response
            body = json.dumps(response.json(), indent=4)
        except ValueError:
            body = response.text
    else:
        body = response.text

    log_msg = (
        f"Request to {response.url} returned status code {response.status_code}\n"
        f"Headers: {response.headers}\n"
        f"Body: {body}"
    )
    logger.info(log_msg)
