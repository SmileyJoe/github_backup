import json
from types import SimpleNamespace
import yaml


class Config:

    @staticmethod
    def load():
        config = Config._load_yaml("config.yaml")
        config["language"] = Config._load_yaml(config["language_file"] + ".yaml")

        return json.loads(json.dumps(config), object_hook=lambda d: SimpleNamespace(**d))

    @staticmethod
    def _load_yaml(file_name):
        file = open(file_name, "r")
        data = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        return data
