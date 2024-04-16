import logging

import spacy
from lib.handlers import OpenAIHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChainPoll:
    def __init__(self, dataset=None, n=5):
        if dataset is None:
            dataset = []
        self.dataset = dataset
        self.n = n
        self.ai_handler = OpenAIHandler()
        self.nlp = spacy.load("en_core_web_sm")
        print(f"Chainpoll initialized")

    def evaluate(self):

        results = []

        for entity in self.dataset:
            question = entity["question"]
            answer = entity["answer"]
            if not answer:
                answer = self.ai_handler.ask_llm(prompt=question)[0]
            prompt = f'''
                Does the following completion contain hallucinations?
                Completion: {answer}
                It was based on this question:
                Question: {question}
                Use chain of thought to explain the completion. Rebuild the completion using your answer and check again if the completion is right.
                It is mandatory that your first word in your response is yes or no as the response of the following question.
                It is mandatory to explain yourself after.
                Does this completion contain hallucinations?
                '''

            response = self.ai_handler.ask_llm(prompt, self.n)
            yes_answers = 0

            for text in response:
                if text.startswith('Yes'):
                    yes_answers += 1

            results.append({
                "question": question,
                "answer": answer,
                "score": yes_answers / self.n
            })

        return results
