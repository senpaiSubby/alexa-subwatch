FROM python:3.7.4-stretch

RUN apt update
RUN apt install ranger neovim htop -y

COPY subwatch/. /app/
WORKDIR /app

RUN mkdir /root/.ssh
RUN ssh-keyscan -H serveo.net > /root/.ssh/known_hosts


RUN pip install -r requirements.txt

VOLUME ["/config"]

ENTRYPOINT /app/start.sh && /bin/bash
