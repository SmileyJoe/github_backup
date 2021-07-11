from pushover import Client


class Log:

    def __init__(self, config):
        self._config = config.logging
        self._pushover = config.pushover
        self._cloned = []
        self._updated = []
        self._skipped = []

    def updated(self, name):
        if self._config.type.updated:
            self._repo(name, self._Colors.YELLOW, "updated")
        self._updated.append(name)

    def skipped(self, name):
        if self._config.type.skipped:
            self._repo(name, self._Colors.RED, "skipped")
        self._skipped.append(name)

    def cloned(self, name):
        if self._config.type.cloned:
            self._repo(name, self._Colors.GREEN, "cloned")
        self._cloned.append(name)

    def pushover(self):
        pushover = Client(self._pushover.user, api_token=self._pushover.api_token)

        count_cloned = len(self._cloned)
        count_skipped = len(self._skipped)
        count_updated = len(self._updated)

        if count_cloned > 0 or count_updated > 0 or count_skipped > 0:
            title = "Success!"

            message = "Cloned: {cloned} \nUpdated: {updated} \nSkipped: {skipped}"\
                .format(cloned=count_cloned,
                        updated=count_updated,
                        skipped=count_skipped)

            message += self._pushover_message("Cloned",
                                              self._pushover.notification_type.cloned,
                                              self._cloned)

            message += self._pushover_message("Updated",
                                              self._pushover.notification_type.updated,
                                              self._updated)

            message += self._pushover_message("Skipped",
                                              self._pushover.notification_type.skipped,
                                              self._skipped)

        else:
            title = "Failed!"

            message = "Something went wrong"

        if len(message) > self._pushover.message_limit:
            append_message = " ..."
            max_len = self._pushover.message_limit - len(append_message)
            message = (message[:max_len] + append_message)

        pushover.send_message(message,
                              title="Github sync {title}".format(title=title),
                              priority=-1)

    def _pushover_message(self, title, log, list_name):
        message = ""

        if log and len(list_name) > 0:
            message += "\n\n{title}:".format(title=title)

            for name in list_name:
                message += "\n{name}".format(name=name)

        return message

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
