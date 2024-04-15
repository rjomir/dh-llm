from datasets import load_dataset
from lib.parsers.parser import Parser


class CovidParser(Parser):
    display_name = 'Covid QA'
    _id = 'covid-qa'

    def __init__(self):
        self.dataset = load_dataset('covid_qa_deepset')
        self.dataset = self.dataset['train']

    def display(self):
        results = []

        for element in self.dataset:
            results.append(
                {
                    'question': element['question'],
                    'context': element['context'],
                    'answer': element['answers']['text'][0],
                    'category': ''
                }
            )
        return results
