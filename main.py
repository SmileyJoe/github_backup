from github import Github
from git import Repo
from print_colors import Colors
from pushover import Client
from config import Config
from db import Db
import os
from datetime import datetime, timezone


config = Config()
db = Db()
github = Github(config.github.token)
pushover = Client(config.pushover.user, api_token=config.pushover.api_token)

last_run = datetime.fromisoformat(db.last_run)
time_start = datetime.now().astimezone(timezone.utc)
count_cloned = 0
count_updated = 0
count_skipped = 0

for repo in github.get_user().get_repos(affiliation="owner", sort="updated", direction="direction"):
    updated_at = repo.updated_at.replace(tzinfo=timezone.utc)

    if last_run < updated_at:
        dir = config.repo_dir + "/" + repo.name

        if not os.path.isdir(dir):
            Repo.clone_from(repo.ssh_url, dir)
            action = Colors.GREEN + "cloned" + Colors.END
            count_cloned += 1
        else:
            Repo(dir).remotes.origin.pull()
            action = Colors.YELLOW + "updated" + Colors.END
            count_updated += 1
    else:
        action = Colors.RED + "skipped" + Colors.END
        count_skipped += 1
    print("{name} : {action}".format(name=repo.name, action=action))

if count_cloned > 0 or count_updated > 0 or count_skipped > 0:
    message = "Cloned: {cloned} \nUpdated: {updated} \nSkipped: {skipped}".format(cloned=count_cloned, updated=count_updated, skipped=count_skipped)
    title = "Success!"
else:
    message = "Something went wrong"
    title = "Failed!"

pushover.send_message(message, title="Github sync {title}".format(title=title), priority=-1)

db.last_run = time_start
db.save()
