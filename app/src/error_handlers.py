import json

import requests
import logging

from src.settings import settings


class HTTPSlackHandler(logging.Handler):
    """Custom slack logger handler."""

    def emit(self, record):
        """
        Send message to slack server.

        :param record: logger record
        :return: post request content
        """
        log_entry = self.format(record)
        json_text = json.dumps({"text": log_entry})
        slack_webhook_key = settings.get_slack_webhook_key()
        url = 'https://hooks.slack.com/services/' + slack_webhook_key
        return requests.post(url, json_text, headers={"Content-type": "application/json"}).content
