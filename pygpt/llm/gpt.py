from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate


class GptApi:
    def __init__(self, api_key: str, model: str, prompt: str, memory: int = 4) -> None:
        self.OPENAI_API_KEY = api_key
        self.OPENAI_MODEL = model

        self.llm = ChatOpenAI(openai_api_key=self.OPENAI_API_KEY, model=model)

        self.chain = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferWindowMemory(k=memory)
        )
        self.prompt_template = prompt
        self.prompt = PromptTemplate.from_template(self.prompt_template)
