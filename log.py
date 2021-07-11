from pushover import Client


class Log:

    def __init__(self, config):
        self._config = config.logging
        self._pushover = config.pushover
        self._count_cloned = 0
        self._count_updated = 0
        self._count_skipped = 0

    def updated(self, name):
        self._repo(name, self._Colors.YELLOW, "updated")
        self._count_updated += 1

    def skipped(self, name):
        self._repo(name, self._Colors.RED, "skipped")
        self._count_skipped += 1

    def cloned(self, name):
        self._repo(name, self._Colors.GREEN, "cloned")
        self._count_cloned += 1

    def pushover(self):
        pushover = Client(self._pushover.user, api_token=self._pushover.api_token)
        if self._count_cloned > 0 or self._count_updated > 0 or self._count_skipped > 0:
            message = "Cloned: {cloned} \nUpdated: {updated} \nSkipped: {skipped}"\
                .format(cloned=self._count_cloned,
                        updated=self._count_updated,
                        skipped=self._count_skipped)
            title = "Success!"
        else:
            message = "Something went wrong"
            title = "Failed!"

        pushover.send_message(message,
                              title="Github sync {title}".format(title=title),
                              priority=-1)

    def _repo(self, name, color, action):
        self.log("{name} : {color}{action}{end_color}"
                 .format(name=name,
                         action=action,
                         color=color,
                         end_color=self._Colors.END))

    def log(self, message):
        if self._config.enabled:
            print(message)

    class _Colors:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        END = '\033[0m'
