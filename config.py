from lib.handlers import OpenAIHandler

llm_handler = None


def init_building_blocks():
    global llm_handler

    if llm_handler is None:
        llm_handler = OpenAIHandler()


init_building_blocks()