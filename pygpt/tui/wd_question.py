from textual.screen import ModalScreen
from textual.containers import Grid
from textual.app import ComposeResult
from textual.widgets import Button, Label


class QuestionWindow(ModalScreen):
    def __init__(self, question) -> None:
        self.question = question 
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.question, id='lbl_question'),
            Button('Ok', variant='error', id='btn_ok_qw'),
            Button('Cancel', variant='primary', id='btn_cancel_qw'),
            id='grid_qw'
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'btn_ok_qw':
            self.dismiss(True)
        else:
            self.dismiss(False)
