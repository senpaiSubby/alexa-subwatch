FROM python:3.7.4-stretch

RUN apt update
RUN apt install ranger neovim htop -y

COPY subwatch/. /app/
WORKDIR /app

RUN pip install -r requirements.txt

VOLUME ["/config"]

CMD [ "python", "./main.py" ]
