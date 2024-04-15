import logging

import requests
from openai import OpenAI, APIError
from requests import RequestException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

base_url = 'http://127.0.0.1:5000'


class OpenAIHandler:
    def __init__(self):
        self.settings = None
        self.client = None

    def fetch_settings(self):
        try:
            response = requests.get('http://127.0.0.1:5000/settings')
            response.raise_for_status()
            self.settings = response.json()
            logger.info("Settings fetched successfully.")

            self.client = OpenAI(api_key=self.settings['openaiKey'])
        except RequestException as e:
            logger.error(f"Failed to fetch settings: {e}")
            raise

    def ask_llm(self, prompt, n=1, temperature=0, max_new_tokens=400):
        try:
            if not self.client:
                self.fetch_settings()

            response = self.client.completions.create(
                prompt=prompt,
                max_tokens=max_new_tokens,
                n=n,
                temperature=temperature,
                model='gpt-3.5-turbo-instruct'
            )

            results = [r.text.strip() for r in response.choices]
            logger.info(f'Prompt responses: {results}')
            return results

        except APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            raise
