from functools import lru_cache
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).resolve().parent / "config.yml"


@lru_cache()
def load_config() -> dict:
    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


def get_config_section(section: str):
    config = load_config()
    return config.get(section)
