import spacy


class SentenceExtractorHandler:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract(self, text=''):
        return [sent.text.strip() for sent in self.nlp(text).sents]
