import logging

import requests
from requests import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_url = 'http://127.0.0.1:5000/'


class DbResource:
    def __init__(self, path):
        self.resourceUrl = base_url + path

    def fetch(self):
        try:
            response = requests.get(self.resourceUrl)
            response.raise_for_status()
            result = response.json()
            logger.info("Data fetched successfully.")
            return result
        except RequestException as e:
            logger.error(f"Failed to fetch data: {e}")
            raise
