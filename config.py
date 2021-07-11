import json


class Config:

    FILE = "config.json"

    def __init__(self):
        file_config = open(self.FILE, "r")
        config = json.load(file_config)
        file_config.close()

        self.github = self._Github(config["github"])
        self.pushover = self._Pushover(config["pushover"])
        self.repo_dir = config["repo_dir"]
        self.logging = self._Logging(config["logging"])

    class _Logging:

        def __init__(self, config):
            self.enabled = config["enabled"]

    class _Pushover:

        def __init__(self, config):
            self.user = config["user"]
            self.api_token = config["api_token"]
            self.message_limit = 1024

    class _Github:

        def __init__(self, config):
            self.token = config["token"]
