import json
from pathlib import Path


class Config:
    def __init__(self):
        config_path = (
            Path(__file__).resolve().parent.parent
            / "config"
            / "config.json"
        )

        with open(config_path, "r") as f:
            self.data = json.load(f)

    def get(self, *keys):
        value = self.data
        for key in keys:
            value = value[key]
        return value


config = Config()