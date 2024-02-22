import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from textual import on
from textual.app import App
from textual.containers import Grid
from textual.widgets import Input, RichLog, Header

load_dotenv()


class TexGPT(App):
    CSS_PATH = 'style.tcss'

    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-3.5-turbo-0125'

    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)

    prompt = ChatPromptTemplate.from_messages([
        ('system', 'You are world class programmer'),
        ('user', '{input}')
    ])
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    def compose(self):
        with Grid():
            yield Header()
            yield RichLog(id='anzeige', classes='anzeige', wrap=True, highlight=True)
            yield Input(placeholder='Enter your question', classes='eingabe')

    def on_mount(self) -> None:
        self.title = '--PyGPT--'

    @on(Input.Submitted)
    def get_answer(self):
        user_input = self.query_one(Input)
        question = {'input': user_input.value}
        result = self.chain.invoke(question)
        rich = self.query_one('#anzeige', RichLog)
        rich.write(f'{user_input.value}\n {result} \n\n')
        user_input.value = ''


if __name__ == "__main__":
    TexGPT().run()
