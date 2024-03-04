import pathlib
import tomli
import tomli_w

config_path = pathlib.Path(__file__).parent / "app_config.toml"


def write_config_file(config: dict):
    with open(config_path, mode="wb") as wfp:
        tomli_w.dump(config, wfp)


def read_config_file():
    with config_path.open(mode="rb") as fp:
        config = tomli.load(fp)
        return config


if not config_path.is_file():
    config_path.touch()
    init_config = {
        'openai_api_key': '',
        'model': 'gpt-3.5-turbo-0125',
        'prompt': 'System: You are world class programmer. Just give back the pure code '
                  'without any explanations or something else. The code as markdown. Give the answer in german.\n'
                  'Human: {question}'
    }
    write_config_file(init_config)

app_config = read_config_file()


