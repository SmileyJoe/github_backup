from github import Github
from git import Repo
from config import Config
from log import Log
from db import Db
import os
from datetime import datetime, timezone


config = Config.load()
db = Db()
log = Log(config)
github = Github(config.github.token)

last_run = datetime.fromisoformat(db.last_run)
time_start = datetime.now().astimezone(timezone.utc)

for repo in github.get_user().get_repos(affiliation="owner", sort="updated", direction="desc"):
    updated_at = repo.updated_at.replace(tzinfo=timezone.utc)

    if last_run < updated_at:
        repo_dir = config.repo_dir + "/" + repo.name

        if not os.path.isdir(repo_dir):
            Repo.clone_from(repo.ssh_url, repo_dir)
            log.cloned(repo.name)
        else:
            Repo(repo_dir).remotes.origin.pull()
            log.updated(repo.name)
    else:
        log.skipped(repo.name)

log.pushover()

db.last_run = time_start
db.save()
