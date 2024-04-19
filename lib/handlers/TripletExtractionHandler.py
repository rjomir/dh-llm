from . import ExtractorBase

LLM_TRIPLET_EXTRACTION_PROMPT_Q = \
    """Given a question and a candidate answer to the question, please extract a KG from the candidate answer 
    condition on the question and represent the KG with triples formatted with ("subject", "predicate", "object"). 
    Please note that this is an EXTRACTION task, so DO NOT care about whether the content of the candidate answer is 
    factual or not, just extract the triplets from it.
    
    Here are some in-context examples:
    
    ### Question:
    Given these paragraphs about the Tesla bot, what is its alias?
    
    ### Candidate Answer: Optimus (or Tesla Bot) is a robotic humanoid under development by Tesla, Inc. It was 
    announced at the company's Artificial Intelligence (AI) Day event on August 19, 2021.
    
    ### KG:
    ("Optimus", "is", "robotic humanoid")
    ("Optimus", "under development by", "Tesla, Inc.")
    ("Optimus", "also known as", "Tesla Bot")
    ("Tesla, Inc.", "announced", "Optimus")
    ("Announcement of Optimus", "occurred at", "Artificial Intelligence (AI) Day event")
    ("Artificial Intelligence (AI) Day event", "held on", "August 19, 2021")
    ("Artificial Intelligence (AI) Day event", "organized by", "Tesla, Inc.")
    
    ### Question:
    here is some text about Andre Weiss, how many years was Andre at University of Dijon in Paris?
    
    ### Candidate Answer:
    11 years
    
    ### KG:
    ("Andre Weiss at University of Dijon in Paris", "duration", "11 years")
    
    
    Now generate the KG for the following candidate answer based on the provided question:
    
    ### Question:
    {q}
    
    ### Candidate Answer:
    {a}
    
    ### KG:
    """

LLM_TRIPLET_EXTRACTION_PROMPT = \
    """Given an input text, please extract a KG from the text and represent the KG with triples formatted with (
    "subject", "predicate", "object"), each triplet in a line. Please note that this is an EXTRACTION task, 
    so DO NOT care about whether the content of the candidate answer is factual or not, just extract the triplets 
    from it.
    
    Here are some in-context examples:
    
    ### Input: Optimus (or Tesla Bot) is a robotic humanoid under development by Tesla, Inc. It was announced at the 
    company's Artificial Intelligence (AI) Day event on August 19, 2021.
    
    ### KG:
    ("Optimus", "is", "robotic humanoid")
    ("Optimus", "under development by", "Tesla, Inc.")
    ("Optimus", "also known as", "Tesla Bot")
    ("Tesla, Inc.", "announced", "Optimus")
    ("Announcement of Optimus", "occurred at", "Artificial Intelligence (AI) Day event")
    ("Artificial Intelligence (AI) Day event", "held on", "August 19, 2021")
    ("Artificial Intelligence (AI) Day event", "organized by", "Tesla, Inc.")
    
    ### Input: The song "Here Comes the Boom" was originally released by American rock band Nelly in 2002 for the 
    soundtrack of the film "The Longest Yard."
    
    ### KG:
    ("The song 'Here Comes the Boom'", "originally released by", "American rock band Nelly")
    ("The song 'Here Comes the Boom'", "released in", "2002")
    ("The song 'Here Comes the Boom'", "featured in", "soundtrack of the film 'The Longest Yard'")
    ("American rock band Nelly", "released", "The song 'Here Comes the Boom'")
    ("The Longest Yard", "had soundtrack featuring", "The song 'Here Comes the Boom'")
    
    
    Now generate the KG for the provided input text:
    
    ### Input:
    {input_text}
    
    ### KG:
    """


class TripletExtractionHandler(ExtractorBase):
    def __init__(
            self,
            llm_handler,
            claim_format: str = 'triplet',
            batch_size=16
    ) -> None:
        super().__init__(claim_format=claim_format)
        if self.claim_format == 'triplet':
            self.prompt_temp_wq = LLM_TRIPLET_EXTRACTION_PROMPT_Q
            self.prompt_temp = LLM_TRIPLET_EXTRACTION_PROMPT

        self.llm_handler = llm_handler
        self.batch_size = batch_size

    def extract_claim_triplets(self, response, question):
        triplets_list = []
        if question is None:
            prompt = self.prompt_temp.format(
                input_text=response
            )
        else:
            prompt = self.prompt_temp_wq.format(
                q=question,
                a=response
            )

        llm_response = self.llm_handler.ask_llm(prompt)
        if llm_response and len(llm_response):
            kg_str = None
            if '###' in llm_response:
                kg_str = llm_response[:llm_response.index('###')]
            else:
                kg_str = llm_response
            triplets = self._parse_claim_triplets(kg_str)
            triplets_list.append(triplets)
        else:
            triplets_list.append([])

        return triplets_list
