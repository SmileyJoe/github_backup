from datetime import datetime, timezone
import os
import json


# Simple json file to be used for storing data between runs
class Db:
    FILE = "db.json"

    def __init__(self):
        # if the file doesn't exist yet, set the defaults
        if not os.path.isfile(self.FILE):
            self._db = {
                "last_run": datetime(1, 1, 1, 0, 0, 0, 0, timezone.utc).isoformat()
            }
        # else parse the json into a dict
        else:
            file = open(self.FILE, "r")
            self._db = json.load(file)
            file.close()

    @property
    # this is a timestamp in UTC+0 in isoformat for the last time the script ran
    # it is used to ignore repos that haven't been updated since when the script is called again
    def last_run(self):
        return self._db["last_run"]

    @last_run.setter
    # sets the property from a datetime object
    def last_run(self, last_run):
        self._db["last_run"] = last_run.isoformat()

    # save the json to the file
    def save(self):
        with open(self.FILE, 'w') as f:
            json.dump(self._db, f, indent=4)