import json
from types import SimpleNamespace


class Config:

    @staticmethod
    def load():
        file_config = open("config.json", "r")
        config = json.load(file_config, object_hook=lambda d: SimpleNamespace(**d))
        file_config.close()
        return config
