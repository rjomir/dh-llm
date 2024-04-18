import logging

from selfcheckgpt.modeling_selfcheck import SelfCheckBERTScore
from .base import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SelfCheckBert(Base):
    def __init__(self, dataset=None):
        super().__init__()
        if dataset is None:
            dataset = []
        self.dataset = dataset
        print(f"SelfCheck-Bert initialized")

    def evaluate(self):
        bert_model = SelfCheckBERTScore()
        results = []

        for entity in self.dataset:
            answer = entity["answer"]
            if not answer:
                answer = self.ask_llm(entity["question"])

            passage = entity["question"] + '.' + answer
            sentences = self.extract_sentence(passage)
            logger.info(sentences)
            bert_pred = bert_model.predict(sentences=sentences, sampled_passages=[passage])
            results.append({
                "question": entity['question'],
                "answer": answer,
                "score": bert_pred.tolist()
            })

        return results
