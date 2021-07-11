from github import Github
from git import Repo
from pushover import Client
from config import Config
from log import Log
from db import Db
import os
from datetime import datetime, timezone


config = Config()
db = Db()
log = Log(config)
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
        repo_dir = config.repo_dir + "/" + repo.name

        if not os.path.isdir(repo_dir):
            Repo.clone_from(repo.ssh_url, repo_dir)
            log.cloned(repo.name)
            count_cloned += 1
        else:
            Repo(repo_dir).remotes.origin.pull()
            log.updated(repo.name)
            count_updated += 1
    else:
        log.skipped(repo.name)
        count_skipped += 1

if count_cloned > 0 or count_updated > 0 or count_skipped > 0:
    message = "Cloned: {cloned} \nUpdated: {updated} \nSkipped: {skipped}".format(cloned=count_cloned, updated=count_updated, skipped=count_skipped)
    title = "Success!"
else:
    message = "Something went wrong"
    title = "Failed!"

pushover.send_message(message, title="Github sync {title}".format(title=title), priority=-1)

db.last_run = time_start
db.save()
