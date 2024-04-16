import logging
import time

import spacy
from lib.handlers import OpenAIHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


prompt = '''
You will be given one question.

Your task is to rate the answer on one metric.

Please make sure you read and understand these instructions carefully. Please keep this document open while 
reviewing, and refer to it as needed.

Evaluation Criteria:

Relevance (1-5) - selection of important content from the question. The answer should include only important 
information from the question. Annotators were instructed to penalize summaries which contained redundancies and 
excess information.

Evaluation Steps:

1. Read the answer and the question carefully. 
2. Compare the answer to the question and identify the main points. 
3. Assess how well the answer covers the main points of the question, and how much irrelevant or redundant information 
it contains. 4. Assign a relevance score from 1 to 5.


Example:


Source Text:

{{Question}}

Summary:

{{Answer}}


Evaluation Form (scores ONLY):

- Relevance:
'''


class GEval:
    def __init__(self, dataset=None, n=5):
        if dataset is None:
            dataset = []
        self.dataset = dataset
        self.n = n
        self.ai_handler = OpenAIHandler()
        self.nlp = spacy.load("en_core_web_sm")
        print(f"G-Eval initialized")

    def evaluate(self):

        results = []
        ct, ignore = 0, 0

        for entity in self.dataset:
            question = entity['question']
            answer = entity['answer']
            if not answer:
                answer = self.ai_handler.ask_llm(prompt=question)[0]
            cur_prompt = prompt.replace('{{Question}}', question).replace('{{Answer}}', answer)
            entity['prompt'] = cur_prompt
            while True:
                try:
                    _response = self.ai_handler.ask_llm(
                        prompt=cur_prompt,
                        temperature=2,
                        max_new_tokens=5,
                        n=20
                    )
                    time.sleep(0.5)

                    all_responses = [_response['choices'][i]['message']['content'] for i in
                                     range(len(_response['choices']))]
                    entity['all_responses'] = all_responses
                    results.append(entity)
                    ct += 1
                    break
                except Exception as e:
                    print(e)
                    if "limit" in str(e):
                        time.sleep(2)
                    else:
                        ignore += 1
                        print('ignored', ignore)

                        break

        return results
