from github import Github
from git import Repo
from secrets import GITHUB_TOKEN, PUSHOVER_TOKEN, PUSHOVER_USER
from print_colors import Colors
from pushover import Client
import os
from datetime import datetime, timezone
import json


FILE_CONFIG = "config.json"
if not os.path.isfile(FILE_CONFIG):
    config = {
        "last_update": datetime(1, 1, 1, 0, 0, 0, 0, timezone.utc).isoformat()
    }
    file_config = open(FILE_CONFIG, "x")
else:
    file_config = open(FILE_CONFIG, "r")
    config = json.load(file_config)

file_config.close()

last_update = datetime.fromisoformat(config["last_update"])
time_start = datetime.now().astimezone(timezone.utc)
count_cloned = 0
count_updated = 0
count_skipped = 0
DIR_REPO = "repos"

github = Github(GITHUB_TOKEN)

for repo in github.get_user().get_repos(affiliation="owner", sort="updated", direction="direction"):
    updated_at = repo.updated_at.replace(tzinfo=timezone.utc)

    if last_update < updated_at:
        dir = DIR_REPO + "/" + repo.name

        if not os.path.isdir(dir):
            Repo.clone_from(repo.ssh_url, dir)
            action = Colors.GREEN + "cloned" + Colors.END
            count_cloned = count_cloned + 1
        else:
            Repo(dir).remotes.origin.pull()
            action = Colors.YELLOW + "updated" + Colors.END
            count_updated = count_updated + 1
    else:
        action = Colors.RED + "skipped" + Colors.END
        count_skipped = count_skipped + 1
    print("{name} : {action}".format(name=repo.name, action=action))

pushover = Client(PUSHOVER_USER, api_token=PUSHOVER_TOKEN)

if count_cloned > 0 or count_updated > 0 or count_skipped > 0:
    message = "Cloned: {cloned} \nUpdated: {updated} \nSkipped: {skipped}".format(cloned=count_cloned, updated=count_updated, skipped=count_skipped)
    title = "Success!"
else:
    message = "Something went wrong"
    title = "Failed!"

pushover.send_message(message, title="Github sync {title}".format(title=title), priority=-1)

config["last_update"] = time_start.isoformat()
with open(FILE_CONFIG, 'w') as f:
    json.dump(config, f, indent=4)
