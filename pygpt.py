import os

from dotenv import load_dotenv

from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input, RichLog, Header, Footer

load_dotenv()


class GptApi:
    def __init__(self, model: str = 'gpt-3.5-turbo-0125'):
        self.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
        self.OPENAI_MODEL = model

        self.llm = ChatOpenAI(openai_api_key=self.OPENAI_API_KEY, model_name=self.OPENAI_MODEL, temperature=0)

        self.chain = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferWindowMemory(k=4),
        )

        self.prompt_template = """
        System: You are world class programmer. Just give back the pure code 
        without any explanations or something else. The code as markdown. Give the answer in german.
        Human: {question}
        """

        self.prompt = PromptTemplate.from_template(self.prompt_template)


class TexGPT(App):
    CSS_PATH = 'style.tcss'

    chat = GptApi()

    BINDINGS = [
        Binding(key="ctrl+c", action="quit", description="Quit the app")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id='view', classes='view', wrap=True, highlight=True)
        yield Input(id='input', placeholder='Enter your question', classes='input')
        yield Footer()

    def on_mount(self) -> None:
        self.title = '--PyGPT--'
        self.set_focus(self.query_one('#input', Input))

    @on(Input.Submitted)
    def get_answer(self):
        user_input = self.query_one('#input', Input)
        question = {'input': self.chat.prompt.format(question=user_input.value)}

        result = self.chat.chain.invoke(question)

        rich = self.query_one('#view', RichLog)
        rich.write(f'{user_input.value}\n\n{result.get('response')}\n\n')
        user_input.value = ''


if __name__ == "__main__":
    TexGPT().run()
