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
  reasonfolder: true
  seriesType: standard
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

### Running the Project

To get the project up and running on AWS Lambda and the Alexa Developer Dashboard, follow these
guides:

- [Setting up the docker container]()
- [Creating the AWS Alexa Skill]()

