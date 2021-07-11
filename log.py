class Log:

    def __init__(self, config):
        self._enabled = config.logging.enabled

    def updated(self, name):
        self._repo(name, self._Colors.YELLOW, "updated")

    def skipped(self, name):
        self._repo(name, self._Colors.RED, "skipped")

    def cloned(self, name):
        self._repo(name, self._Colors.GREEN, "cloned")

    def _repo(self, name, color, action):
        self.log("{name} : {color}{action}{end_color}"
                 .format(name=name,
                         action=action,
                         color=color,
                         end_color=self._Colors.END))

    def log(self, message):
        if self._enabled:
            print(message)

    class _Colors:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        END = '\033[0m'
