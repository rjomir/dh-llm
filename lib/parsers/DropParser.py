from datasets import load_dataset
from lib.parsers.parser import Parser


class DropParser(Parser):
    display_name = 'Drop'
    _id = 'drop'

    def __init__(self):
        self.dataset = load_dataset("EleutherAI/drop")
        self.dataset = self.dataset['train']

    def display(self):
        results = []

        for element in self.dataset:
            answer_spans = element['answer']['spans']
            answer_number = element['answer']['number']
            answer_date = element['answer']['date']

            results.append(
                {
                    'question': element['question'],
                    'context': element['passage'],
                    'answer': answer_spans[0] if len(answer_spans) > 0
                    else answer_number if answer_number
                    else answer_date['day'] + '-' + answer_date['month'] + '-' + answer_date[
                        'year'] if answer_date
                    else None,
                    'category': ''
                }
            )
        return results
