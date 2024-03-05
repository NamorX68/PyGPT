from textual import on
from textual.reactive import reactive
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input, RichLog, Header, Footer

from pygpt.tui.wd_config import ConfigWindow
from pygpt.tui.wd_question import QuestionWindow
from pygpt.tui.wd_message import MessageWindow
from pygpt.llm.gpt import GptApi

from pygpt.config import app_config, read_config_file


class TexGPT(App):
    CSS_PATH = 'style.tcss'

    BINDINGS = [
        Binding('ctrl+q', 'request_quit', 'Quit'),
        Binding('ctrl+s', 'request_config', 'Settings', priority=True, show=True)
    ]

    win_titel = reactive('--PyGPT--')

    def __init__(self, config: dict):
        super().__init__()
        self.app_config = config
        self.chat = self.open_ai_chat()

    def open_ai_chat(self):
        if self.app_config.get('openai_api_key') != '':
            chat = GptApi(
                self.app_config.get('openai_api_key'),
                self.app_config.get('model', 'gpt-3.5-turbo-0125'),
                self.app_config.get('prompt'),
                self.app_config.get('memory', 4)
            )
        else:
            chat = None
        return chat

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield RichLog(id='view', wrap=True, highlight=True)
        yield Input(id='input', placeholder='Enter your question')

        yield Footer()

    def on_mount(self) -> None:
        self.title = self.win_titel
        self.set_focus(self.query_one('#input', Input))

    def action_request_quit(self) -> None:
        def check_ok(ok: bool):
            if ok:
                self.app.exit()
        self.push_screen(QuestionWindow('Are u sure?'), check_ok)

    def action_request_config(self) -> None:
        def check_save(save: bool):
            if save:
                self.app_config = read_config_file()
                self.chat = self.open_ai_chat()

        self.push_screen(ConfigWindow(self.app_config), check_save)

    @on(Input.Submitted, '#input')
    def get_answer(self, input_field: Input) -> None:
        try:
            question = {'input': self.chat.prompt.format(question=input_field.value)}

            result = self.chat.chain.invoke(question)

            rich = self.query_one('#view', RichLog)
            response = result.get('response')
            rich.write(f'''{input_field.value}\n\n{response}\n\n''')

            self.query_one('#input').value = ''

        except Exception as e:
            self.query_one('#input', Input).value = ''
            self.push_screen(MessageWindow('No OPENAI_API_KEY was stored or the key is incorrect. '
                                           'Open the settings and check the OPENAI_API_KEY'))


def main():
    TexGPT(app_config).run()


if __name__ == "__main__":
    main()
