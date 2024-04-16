import logging

from openai import OpenAI, APIError
from .DbResource import DbResource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIHandler:
    def __init__(self):
        self.client = None
        self.settings = None
        self.settings_db_resource = DbResource('settings')

    def ask_llm(self, prompt, n=1, temperature=0, max_new_tokens=400):
        try:
            if not self.client:
                self.settings = self.settings_db_resource.fetch()
                self.client = OpenAI(api_key=self.settings['openaiKey'])

            if self.settings["openaiMaxTokens"]:
                max_new_tokens = self.settings["openaiMaxTokens"]

            response = self.client.completions.create(
                prompt=prompt,
                max_tokens=int(max_new_tokens),
                n=n,
                temperature=temperature,
                model=self.settings["openaiModel"]
            )

            results = [r.text.strip() for r in response.choices]
            logger.info(f'Prompt responses: {results}')
            return results

        except APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            raise
