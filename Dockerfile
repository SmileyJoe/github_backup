FROM python:3.10

RUN apt-get update && apt-get -y install cron vim

WORKDIR /github/app
COPY ./app /github/app

RUN pip install -r requirements.txt
COPY crontab /etc/cron.d/github_backup

RUN chmod 0644 /etc/cron.d/github_backup
RUN /usr/bin/crontab /etc/cron.d/github_backup

# run crond as main process of container
CMD ["cron", "-f"]