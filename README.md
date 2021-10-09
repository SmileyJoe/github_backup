# Github backup
TEST
Python script that will clone all repos owned by the user token, private and public, or pull in any updates if the repo is already cloned.

Note:
This is meant as a backup, the repos it clones should not be updated as there is nothing in place to handle conflicts or to push up changes

## Setup

- Duplicate `example_config.yaml` and rename it to `config.yaml`
- Update `config.yaml` with your keys/settings
- Install the requirements with `pip install -r requirements.txt`
- See [here](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token) for generating a github token
- For the pushover api token, a new app will need to be registered [here](https://pushover.net/apps/build)

## Translations

- Copy a language file, rename the 2 letter code and translate it, the file can them be specified in `config.yaml`

## Libraries

- [PyGithub](https://github.com/PyGithub/PyGithub)
- [GitPython](https://github.com/gitpython-developers/GitPython)
- [python-pushover](https://github.com/Thibauth/python-pushover)
- [pyyaml](https://github.com/yaml/pyyaml)
