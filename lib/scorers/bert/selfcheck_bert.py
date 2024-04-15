import spacy
from selfcheckgpt.modeling_selfcheck import SelfCheckBERTScore
from lib.handlers import OpenAIHandler


class SelfCheckBert:
    def __init__(self, dataset=None):
        if dataset is None:
            dataset = []
        self.ai_handler = OpenAIHandler()
        self.dataset = dataset
        self.nlp = spacy.load("en_core_web_sm")
        print(f"SelfCheck-Bert initialized")

    def evaluate(self):
        bert_model = SelfCheckBERTScore()
        results = []

        for entity in self.dataset:
            answer = entity["answer"]
            if not answer:
                answer = self.ai_handler.ask_llm(prompt=entity["question"])[0]

            passage = entity["question"] + '.' + answer
            sentences = [sent.text.strip() for sent in self.nlp(passage).sents]
            bert_pred = bert_model.predict(sentences=sentences, sampled_passages=[passage])
            results.append({
                "question": entity['question'],
                "answer": answer,
                "score": bert_pred.tolist()
            })

        return results
