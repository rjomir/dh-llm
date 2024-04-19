from .base import Base
from config import retriever_handler

LLM_CHECKING_PROMPT_Q = \
    """I have a claim that made by a language model to a question, please help me for checking whether the claim can 
    be entailed according to the provided reference which is related to the question. The reference is a list of 
    passages, and the claim is represented as a triplet formatted with ("subject", "predicate", "object").

If the claim is supported by ANY passage in the reference, answer 'Entailment'. If NO passage in the reference entail 
the claim, and the claim is contradicted with some passage in the reference, answer 'Contradiction'. If NO passage 
entail or contradict with claim, or DOES NOT contain information to verify the claim, answer 'Neutral'.

Please DO NOT use your own knowledge for the judgement, just compare the reference and the claim to get the answer.

### Question:
{question}

### Reference:
{reference}

### Claim:
{claim}

Your answer should always be only a single word in ['Entailment', 'Neutral', 'Contradiction']. DO NOT add 
explanations or you own reasoning to the output."""


class RefChecker(Base):
    def __init__(self, dataset=None):
        super().__init__()
        if dataset is None:
            dataset = []
        self.dataset = dataset
        self.label_entailment = 'Entailment'
        self.label_neutral = 'Neutral'
        self.label_contradiction = 'Contradiction'
        self.labels = ["Entailment", "Neutral", "Contradiction"]
        self.prompt_temp_wq = LLM_CHECKING_PROMPT_Q

    def evaluate(self):
        results = []

        for entity in self.dataset:
            question = entity["question"]
            answer = entity["answer"]
            if not answer:
                answer = self.ask_llm(prompt=question)

            reference = retriever_handler._query_google(question)

            prompt = self.prompt_temp_wq.format(
                question=question,
                reference=reference,
                claim=answer
            )

            llm_response = self.ask_llm(
                prompt=prompt,
                temperature=0,
                max_new_tokens=10,
            )

            if self.label_contradiction.lower() in llm_response.lower():
                label = self.label_contradiction
            elif self.label_entailment.lower() in llm_response.lower():
                label = self.label_entailment
            else:
                label = self.label_neutral

            results.append({
                "question": question,
                "answer": answer,
                "score": label
            })

        return results
