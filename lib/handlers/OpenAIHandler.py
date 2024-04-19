import logging

from openai import OpenAI, APIError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIHandler:
    def __init__(self, settings_handler):
        self.settings = None
        self.client = None
        self.settings_handler = settings_handler

    def ask_llm(self, prompt, n=1, temperature=0, max_new_tokens=400):
        try:
            if not self.client:
                self.settings = self.settings_handler.fetch()["content"]
                self.client = OpenAI(api_key=self.settings['OPEN_AI_KEY'])

            if self.settings["OPEN_AI_MAX_TOKENS"]:
                max_new_tokens = self.settings["OPEN_AI_MAX_TOKENS"]

            response = self.client.completions.create(
                prompt=prompt,
                max_tokens=int(max_new_tokens),
                n=n,
                temperature=temperature,
                model=self.settings["OPEN_AI_MODEL"]
            )

            results = [r.text.strip() for r in response.choices]
            logger.info(f'Prompt responses: {results}')
            return results

        except APIError as e:
            logger.error(f"OpenAI API Error: {e}")
            raise
