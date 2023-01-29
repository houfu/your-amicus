from langchain import PromptTemplate, LLMChain, OpenAI

template = """
You are very knowledgeable about legal. You are very friendly and eager to share your knowledge.
It is important to you that I am satisfied with your answers. You are a lawyer but not my lawyer.

Q. {prompt}
A.
"""


class DefaultChain(LLMChain):

    def __init__(self):
        super().__init__(
            llm=OpenAI(),
            prompt=PromptTemplate(input_variables=["prompt"],
                                  template=template)
        )
