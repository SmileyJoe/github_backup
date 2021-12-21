import json
from types import SimpleNamespace
import yaml
import os


# Loads in the yaml config
#
# Usage:
# config = Config().load()
class Config:

    @staticmethod
    # Load the config
    def load():
        # load the config into a dict
        config = Config._load_yaml("config.yaml")
        # using the language_file config, load the language file into a dict
        config["language"] = Config._load_yaml(config["language_file"] + ".yaml")

        # convert the dict to json, then parse the json into an object, this
        # lets us reference config as config.repo_dir instead of config["repo_dir"]
        return json.loads(json.dumps(config), object_hook=lambda d: SimpleNamespace(**d))

    @staticmethod
    # Parse the given yaml file into a dict
    def _load_yaml(file_name):
        file = open(os.path.join(os.path.dirname(__file__), file_name), "r")
        data = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        return data
