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
# github gives us the pushed time back in utc+0, so we need to set that here
time_start = datetime.now().astimezone(timezone.utc)

for repo in github.get_user().get_repos(affiliation="owner", sort="pushed", direction="desc"):
    # pushed at is in utc+0, but it is not explicitly set, so it can't be compared
    # to a datetime where it is set, so we need to replace the timezone settings
    pushed_at = repo.pushed_at.replace(tzinfo=timezone.utc)

    # only handle the repo if it was update since the scripts last run
    if last_run < pushed_at:
        repo_dir = config.repo_dir + "/" + repo.name

        # if the path is not set, we need to clone the repo
        if not os.path.isdir(repo_dir):
            repo_url = "https://{username}:{password}@github.com/{repo_name}.git".format(
                username=config.github.username,
                password=config.github.token,
                repo_name=repo.full_name)
            Repo.clone_from(repo_url, repo_dir)
            log.cloned(repo.name)
        # else we need to pull the new contents
        else:
            Repo(repo_dir).remotes.origin.pull()
            log.updated(repo.name)
    else:
        log.skipped(repo.name)

# send the pushover message
log.pushover()

# save the time the script started
db.last_run = time_start
db.save()
