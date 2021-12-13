# Github backup
Python script that will clone all repos owned by the user token, private and public, or pull in any updates if the repo is already cloned.

Note:
This is meant as a backup, the repos it clones should not be updated as there is nothing in place to handle conflicts or to push up changes

## Setup

- Copy `example_config.yaml` into `app/` and rename it to `config.yaml`
- Update `config.yaml` with your keys/settings
- See [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) for generating a github token
- For the pushover api token, a new app will need to be registered [here](https://pushover.net/apps/build)

## Docker

- Update `Dockerfile` and `docker-compose.yml` to reference the local directory the repos will be cloned to
- Run the container with `docker-compose up -d`

## Without docker

- Install the requirements with `pip install -r requirements.txt`
- Run with `python app/main.py`

## Translations

- Copy a language file, rename the 2 letter code and translate it, the file can them be specified in `config.yaml`

## Libraries

- [PyGithub](https://github.com/PyGithub/PyGithub)
- [GitPython](https://github.com/gitpython-developers/GitPython)
- [python-pushover](https://github.com/Thibauth/python-pushover)
- [pyyaml](https://github.com/yaml/pyyaml)
