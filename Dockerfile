FROM python:3.10

RUN apt-get update && apt-get -y install cron vim

WORKDIR /github/app
COPY ./app /github/app
COPY ./repos /github/repos

RUN pip install -r requirements.txt
COPY crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]