from datetime import datetime, timezone
import os
import json


class Db:
    FILE = "db.json"

    def __init__(self):
        if not os.path.isfile(self.FILE):
            self._db = {
                "last_run": datetime(1, 1, 1, 0, 0, 0, 0, timezone.utc).isoformat()
            }
        else:
            file = open(self.FILE, "r")
            self._db = json.load(file)
            file.close()

    @property
    def last_run(self):
        return self._db["last_run"]

    @last_run.setter
    def last_run(self, last_run):
        self._db["last_run"] = last_run.isoformat()

    def save(self):
        with open(self.FILE, 'w') as f:
            json.dump(self._db, f, indent=4)