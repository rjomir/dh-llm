from lib.handlers import SentenceExtractorHandler, OpenAIHandler, DbResourceHandler, GoogleRetrieverHandler, \
    TripletExtractionHandler

llm_handler = None
sentence_extractor_handler = None
settings_handler = None
retriever_handler = None
triplet_extractor_handler = None


def init_building_blocks(force=False):
    global llm_handler, sentence_extractor_handler, settings_handler, retriever_handler, triplet_extractor_handler

    if llm_handler is None or force:
        sentence_extractor_handler = SentenceExtractorHandler()
        settings_handler = DbResourceHandler('settings')
        llm_handler = OpenAIHandler(settings_handler)
        retriever_handler = GoogleRetrieverHandler(sentence_extractor_handler, settings_handler)
        triplet_extractor_handler = TripletExtractionHandler(llm_handler)


init_building_blocks(force=True)
