import pyperclip as pc

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Footer, Header, Input, RichLog

from pygpt.config import app_config, read_config_file
from pygpt.llm.gpt import GptApi
from pygpt.tui.wd_config import ConfigWindow
from pygpt.tui.wd_message import MessageWindow
from pygpt.tui.wd_question import QuestionWindow

import openai


class TexGPT(App):
    CSS_PATH = "style.tcss"

    BINDINGS = [
        Binding("ctrl+q", "request_quit", "Quit"),
        Binding("ctrl+s", "request_config", "Settings", priority=True, show=True),
    ]

    win_titel = reactive("--PyGPT--")

    def __init__(self, config: dict):
        super().__init__()
        self.app_config = config
        self.chat = self.open_ai_chat()

    def open_ai_chat(self):
        if self.app_config.get("openai_api_key") != "":
            chat = GptApi(
                self.app_config.get("openai_api_key", None),
                self.app_config.get("model", "gpt-3.5-turbo-0125"),
                self.app_config.get("temperature", '0'),
                self.app_config.get("prompt", ''),
                self.app_config.get("memory", '4'),
            )
        else:
            chat = None
        return chat

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        yield RichLog(id="view", wrap=True, highlight=True)
        yield Input(id="input", placeholder="Enter your question")

        yield Footer()

    def on_mount(self) -> None:
        self.title = self.win_titel
        self.set_focus(self.query_one("#input", Input))

    def action_request_quit(self) -> None:
        def check_ok(ok: bool):
            if ok:
                self.app.exit()

        self.push_screen(QuestionWindow("Are u sure?"), check_ok)

    def action_request_config(self) -> None:
        def check_save(save: bool):
            if save:
                self.app_config = read_config_file()
                self.chat = self.open_ai_chat()

        self.push_screen(ConfigWindow(self.app_config), check_save)

    @on(Input.Submitted, "#input")
    def get_answer(self, input_field: Input) -> None:
        try:
            question = {"input": self.chat.prompt.format(question=input_field.value)}

            result = self.chat.chain.invoke(question)

            rich = self.query_one("#view", RichLog)
            response = result.get("response")
            rich.write(f"""{input_field.value}\n\n{response}\n\n""")
            pc.copy(response)
            self.query_one("#input").value = ""

        except openai.OpenAIError as e:
            self.query_one("#input", Input).value = ""
            self.push_screen(
                MessageWindow("Open the settings and check the OPENAI_API_KEY\n\n " f"{e}")
            )
        except Exception as e:
            self.query_one("#input", Input).value = ""
            self.push_screen(
                MessageWindow(f"{e}")
            )


def main():
    TexGPT(app_config).run()


if __name__ == "__main__":
    main()
