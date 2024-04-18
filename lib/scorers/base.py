from config import llm_handler, sentence_extractor_handler, settings_handler


class Base:
    def __init__(self):
        self.settings = settings_handler.fetch()["content"]

    @classmethod
    def ask_llm(cls, prompt, n=1, temperature=0, max_new_tokens=400):
        response = llm_handler.ask_llm(prompt=prompt, n=n, temperature=temperature, max_new_tokens=max_new_tokens)
        return response[0]

    @classmethod
    def extract_sentence(cls, text):
        return sentence_extractor_handler.extract(text)
