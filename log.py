from pushover import Client


# class to handle logging, to the terminal and to pushover etc
# logs are done based on the config settings
class Log:

    def __init__(self, config):
        self._config = config.logging
        self._pushover = config.pushover
        self._language = config.language
        self._cloned = []
        self._updated = []
        self._skipped = []

    # used when a repo is updated
    def updated(self, name):
        if self._config.type.updated:
            self._repo(name, self._Colors.YELLOW, self._language.status.updated)
        self._updated.append(name)

    # used when a repo is skipped
    def skipped(self, name):
        if self._config.type.skipped:
            self._repo(name, self._Colors.RED, self._language.status.skipped)
        self._skipped.append(name)

    # used when a repo is cloned
    def cloned(self, name):
        if self._config.type.cloned:
            self._repo(name, self._Colors.GREEN, self._language.status.cloned)
        self._cloned.append(name)

    # send a notification via pushover
    #
    # notification can have counts of actions as well as lists of repos per action
    def pushover(self):
        pushover = Client(self._pushover.user, api_token=self._pushover.api_token)

        count_cloned = len(self._cloned)
        count_skipped = len(self._skipped)
        count_updated = len(self._updated)

        # if nothing is changed, we assume something failed
        if count_cloned > 0 or count_updated > 0 or count_skipped > 0:
            title = self._language.pushover.success.title

            message = self._language.pushover.success.message.\
                format(count_cloned=count_cloned,
                       count_updated=count_updated,
                       count_skipped=count_skipped,
                       list_cloned=self._pushover_message(self._language.status.cloned,
                                                          self._pushover.notification_type.cloned,
                                                          self._cloned),
                       list_updated=self._pushover_message(self._language.status.updated,
                                                           self._pushover.notification_type.updated,
                                                           self._updated),
                       list_skipped=self._pushover_message(self._language.status.skipped,
                                                           self._pushover.notification_type.skipped,
                                                           self._skipped))

        else:
            title = self._language.pushover.fail.title
            message = self._language.pushover.fail.message

        # if the message is to long, truncate it and add ellipsis
        if len(message) > self._pushover.message_limit:
            append_message = " ..."
            max_len = self._pushover.message_limit - len(append_message)
            message = (message[:max_len] + append_message)

        # send the message as low priority
        pushover.send_message(message,
                              title=self._language.pushover.title.format(title=title),
                              priority=-1,
                              html=1)

    # cycle the list of repos and build the message
    def _pushover_message(self, title, log, list_name):
        message = ""

        if log and len(list_name) > 0:
            message += "\n<b><u>{title}:</u></b>\n".format(title=title)

            for name in list_name:
                message += "{name}\n".format(name=name)

        return message

    # log a repo being processed
    def _repo(self, name, color, action):
        self.log("{name} : {color}{action}{end_color}"
                 .format(name=name,
                         action=action,
                         color=color,
                         end_color=self._Colors.END))

    # log a message to the terminal
    def log(self, message):
        if self._config.enabled:
            print(message)

    # colours used in terminal logs
    class _Colors:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        END = '\033[0m'
