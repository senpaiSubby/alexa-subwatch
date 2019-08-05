# Alexa Subwatch skill


Ask [Alexa](http://alexa.design) to add movie and shows to Radarr and Sonarr.


This Alexa skill will allow you to add movies and TV series to Sonarr and Radarr. Lets be lazy together.

Ask Alexa a few of the following things:

> Alexa, ask Subwatch to add the movie The Star Wars
> Alexa, ask Subwatch to add the show Mr. Robot

### Subwatch Configuration
When the project is first ran a file name `config.yaml` will be created next to the runtime files when you can configure all your settings for Radarr/Sonarr.
```
radarr:
  API: 2111350a0b7512f0a360410abee113fe
  autosearch: true
  monitored: true
  profile: 6
  url: https://radarr.yourwebsite.com
sonarr:
  API: 7cae34ece13e111cf81362621ada9afd
  autosearch: true
  monitored: true
  profile: 6
  seasonfolder: true
  seriesType: standard # standard/anime
  url: https://sonarr.yourwebsite.com
sortingMode: rating # sort results by "rating" or "year"
```


### Docker Compose Image
```yml
version: "3"
services:
  alexa-subwatch:
    image: simplysublime/alexa-subwatch:latest
    container_name: alexa-subwatch
    volumes:
      - ./subwatch:/config
    ports:
      - 5000:5000
    restart: unless-stopped

  serveo:
    image: simplysublime/serveo:latest
    container_name: alexa-subwatch-serveo
    tty: true
    stdin_open: true
    # see https://serveo.net/ for more options
    command: autossh -M 0 -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -o StrictHostKeyChecking=no -R 443:alexa-subwatch:5000 serveo.net
```


### Running the Project

To get the project up and running on AWS Lambda and the Alexa Developer Dashboard, follow these
guides:

- [Setting up the docker container]()
- [Creating the AWS Alexa Skill]()
