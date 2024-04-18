from lib.handlers import SentenceExtractorHandler, OpenAIHandler, DbResourceHandler

llm_handler = None
sentence_extractor_handler = None
settings_handler = None


def init_building_blocks(force=False):
    global llm_handler, sentence_extractor_handler, settings_handler

    if llm_handler is None or force:
        sentence_extractor_handler = SentenceExtractorHandler()
        settings_handler = DbResourceHandler('settings')
        llm_handler = OpenAIHandler()


init_building_blocks(force=True)
