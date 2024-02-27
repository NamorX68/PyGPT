from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Header, Footer, RichLog


class VerticalLayoutExample(App):
    CSS_PATH = "vertical_layout.tcss"

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(classes="box")
        yield Input(placeholder='Enter your question', classes='view')
        yield Footer()


if __name__ == "__main__":
    app = VerticalLayoutExample()
    app.run()