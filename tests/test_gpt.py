import os

from dotenv import load_dotenv

from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_MODEL = 'gpt-3.5-turbo-0125'

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name=OPENAI_MODEL)

conversation_with_summary = ConversationChain(
    llm=llm,
    # We set a low k=2, to only keep the last 2 interactions in memory
    memory=ConversationBufferWindowMemory(k=4),
    verbose=True
)


def main():
    while True:
        question = input("> ")
        answer = conversation_with_summary.predict(input=question)
        print(answer)


if __name__ == "__main__":
    main()
