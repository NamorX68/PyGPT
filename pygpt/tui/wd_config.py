from textual import on
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.containers import Grid
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label, Header, TextArea

from pygpt.config import write_config_file


class ConfigWindow(ModalScreen[bool]):
    win_titel = reactive('settings')

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    def compose(self) -> ComposeResult:
        yield Grid(
            Header(),

            Label('API Key', id='lbl_api_key'),
            Input(id='inp_api_key', placeholder='sk-xxxxx....'),

            Label('Model', id='lbl_model'),
            Input(id='inp_model', placeholder='llm....'),

            Label('Memory', id='lbl_memory'),
            Input(id='inp_memory'),

            Label('Temperature', id='lbl_temperature'),
            Input(id='inp_temperature'),

            Label('Prompt', id='lbl_prompt'),
            TextArea(id='inp_prompt'),

            Button('Save', variant='primary', id='btn_save_cw'),
            Button('Cancel', variant='error', id='btn_cancel_cw'),

            id='grd_cw'
        )

    def on_mount(self) -> None:
        self.title = self.win_titel
        self.query_one('#inp_api_key', Input).value = self.config.get('openai_api_key')
        self.query_one('#inp_model', Input).value = self.config.get('model')
        self.query_one('#inp_memory', Input).value = self.config.get('memory')
        self.query_one('#inp_temperature', Input).value = self.config.get('temperature')
        self.query_one('#inp_prompt', TextArea).insert(self.config.get('prompt'))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'btn_save_cw':
            self.config['openai_api_key'] = self.query_one('#inp_api_key', Input).value
            self.config['model'] = self.query_one('#inp_model', Input).value
            self.config['memory'] = self.query_one('#inp_memory', Input).value
            self.config['temperature'] = self.query_one('#inp_temperature', Input).value
            self.config['prompt'] = self.query_one('#inp_prompt', TextArea).document.text
            write_config_file(self.config)
            self.dismiss(True)
        else:
            self.dismiss(False)

    @on(Input.Submitted, '#inp_api_key')
    def test(self, input_field: Input) -> None:
        model = self.query_one('#inp_model', Input)
        model.value = input_field.value
