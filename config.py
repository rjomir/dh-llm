import os

from lib.handlers.OpenAIHandler import OpenAIHandler

llm_handler = None
triplets_extractor = None
sentence_extractor = None
question_generator = None
retriever = None
checker = None
bertscore = None
ngramscrore = None

def init():
    init_building_blocks()


def init_building_blocks(force=False):
    global llm_handler, triplets_extractor, sentence_extractor, question_generator, \
        retriever, checker, bertscore, ngramscrore

    if llm_handler is None or force:
        llm_handler = OpenAIHandler()
