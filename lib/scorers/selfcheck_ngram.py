from selfcheckgpt.modeling_ngram import UnigramModel, NgramModel
from .base import Base


class SelfCheckNgram(Base):
    def __init__(self, n: int, lowercase: bool = True, dataset=None):
        super().__init__()
        if dataset is None:
            dataset = []
        self.n = n
        if self.settings and hasattr(self.settings, "NGRAM_SAMPLING_NUMBER"):
            self.n = self.settings["NGRAM_SAMPLING_NUMBER"]
        self.lowercase = lowercase
        self.dataset = dataset

        print(f"SelfCheck-{n}gram initialized")

    def evaluate(self):
        if self.n == 1:
            ngram_model = UnigramModel(lowercase=self.lowercase)
        elif self.n > 1:
            ngram_model = NgramModel(n=self.n, lowercase=self.lowercase)
        else:
            raise ValueError("n must be integer >= 1")

        results = []

        for entity in self.dataset:
            answer = entity["answer"]
            if not answer:
                answer = self.ask_llm(prompt=entity["question"])[0]
            passage = entity["question"] + '.' + answer
            ngram_model.add(passage)
            ngram_model.train()
            sentences = self.extract_sentence(passage)
            ngram_pred = ngram_model.evaluate(sentences=sentences)

            results.append({
                "question": entity['question'],
                "answer": answer,
                "score": ngram_pred['sent_level']['avg_neg_logprob']
            })

        return results
