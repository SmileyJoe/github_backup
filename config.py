import json
from types import SimpleNamespace
import yaml


class Config:

    @staticmethod
    def load():
        file_config = open("config.yaml", "r")
        config = yaml.load(file_config, Loader=yaml.FullLoader)
        file_config.close()
        return json.loads(json.dumps(config), object_hook=lambda d: SimpleNamespace(**d))


