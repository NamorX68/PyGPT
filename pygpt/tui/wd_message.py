from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class MessageWindow(ModalScreen):
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.msg, id='lbl_msg'),
            Button('Ok', variant='error', id='btn_ok_msg'),
            id='grid_msg'
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'btn_ok_msg':
            self.app.pop_screen()
