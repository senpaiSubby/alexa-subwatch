
# _____  _              _       _____       _    _  _
# |   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
# |__   || ||     || . || || | ||__   || | || . || || ||     || -_|
# |_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|


import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request
from gevent.pywsgi import WSGIServer
# * Our backends for searching and adding media
from backends.radarr import addMovie, searchMovie, radarrTest
from backends.sonarr import addSeries, searchSeries, sonarrTest


from subprocess import run
from os import path
import yaml
import json
from datetime import datetime
from time import sleep

now = datetime.now()
now = now.strftime("%b/%d/%y %H:%m:%S")

configFile = "config.yaml"
#configFile = "/config/config.yaml"

def createConfig():
    createConfig = {
        "sortingMode": "year",
        "radarr": {
            "url": "https://radarr.atriox.io",
            "API": "",
            "profile": 6,
            "monitored": True,
            "autosearch": True,
            "seriesType": "standard",
            "reasonfolder": True,
        },
        "sonarr": {
            "url": "https://sonarr.atriox.io",
            "API": "",
            "profile": 6,
            "monitored": True,
            "autosearch": True,
            "seriesType": "standard",
            "seasonfolder": True,
        },
        "ombi": {
            "API": "",
            "language": "en",
        },

    }

    with open(configFile, "w") as f:
        yaml.dump(createConfig, f, default_flow_style=False)


# ! CLEAN THIS UP LATER
if not path.isfile(configFile):
    createConfig()

else:
    with open(configFile, 'r', encoding="utf8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        sortingMode = config["sortingMode"]
        radarr_api = config["radarr"]["API"]
        radarr_url = config["radarr"]["url"]
        radarr_profile = config["radarr"]["profile"]
        radarr_monitored = config["radarr"]["monitored"]
        radarr_autosearch = config["radarr"]["autosearch"]
        sonarrAPI = config["sonarr"]["API"]
        sonarr_url = config["sonarr"]["url"]
        sonarr_profile = config["sonarr"]["profile"]
        sonarr_monitored = config["sonarr"]["monitored"]
        sonarr_autosearch = config["sonarr"]["autosearch"]
        sonarr_seriesType = config["sonarr"]["seriesType"]
        sonarr_seasonfolder = config["sonarr"]["seasonfolder"]
        #ombiAPI = config["ombi"]["API"]
        #ombi_language = config["ombi"]["language"]


def clear():
    run(['clear'])


app = Flask(__name__)
ask = Ask(app, "/")

#logging.getLogger("flask_ask").setLevel(logging.DEBUG)


# ! DONT FORGET TO ADD NEW OPTIONS FOR THE INITAL MENU AND MAKE HELP SECTION!
@ask.launch
def launch():
    speech_text = "Welcome to Sub Watch. You can say things like, add a movie, or, add a series, followed by the name of what you want."
    reprompt_text = "I didn't catch that. You can say things like, add a movie, or, add a series, followed by the name of what you want."
    return question(speech_text).reprompt(reprompt_text).reprompt(reprompt_text)

@ask.intent("addMovie")
def searchForMovie(movie):
    # * Tells the session what we are going to be searching for
    session.attributes["mediaType"] = "movie"
    # * Get all results for search term from Radarr in Json format
    results = searchMovie(movie, radarr_api, radarr_url, sortingMode)

    # * If there are multiple results iterate through and make a count of them
    amount_of_results = len(results)

    # * If we have less than 2 results pick the best match
    if amount_of_results >= 3:
        session.attributes["movie"] = movie
        session.attributes["aResults"] = amount_of_results
        session.attributes["results"] = results
        session.attributes["plogic"] = 0

        session.attributes["page"] = 1
        return pickResults()

    elif amount_of_results < 3:
        try:
            movie = results[0]["title"]
            year = results[0]["year"]
            return statement(f"I've added {movie} from {year} to Radarr")
        except IndexError:
            return question(f"Sorry, please try that again")
    else:
        return question(f"Sorry, please try that again")


@ask.intent("addSeries")
def searchForSeries(series):
    # * Tells the session what we are going to be searching for
    session.attributes["mediaType"] = "series"
    # * Get all results for search term from Radarr in Json format
    results = searchSeries(series, sonarrAPI, sonarr_url, sortingMode)

    # * If there are multiple results iterate through and make a count of them
    amount_of_results = len(results)

    # * If we have less than 2 results pick the best match
    if amount_of_results >= 3:
        session.attributes["series"] = series
        session.attributes["aResults"] = amount_of_results
        session.attributes["results"] = results
        session.attributes["plogic"] = 0
        session.attributes["page"] = 1
        return pickResults()

    elif amount_of_results < 3:
        try:
            series = results[0]["title"]
            year = results[0]["year"]
            return statement(f"I've added the series, {series} from {year} to Sonarr")
        except IndexError:
            return question(f"Sorry, please try that again")
    else:
        return question(f"Sorry, please try that again")


@ask.intent("YesIntent")
def pickResults():
    mediaType = session.attributes["mediaType"]

    if mediaType == "movie":
        originalMovie = session.attributes["movie"]
        aResults = session.attributes["aResults"]
        results = session.attributes["results"]
        movie1 = results[0]["title"]
        movie1_year = results[0]["year"]
        movie2 = results[1]["title"]
        movie2_year = results[1]["year"]
        movie3 = results[2]["title"]
        movie3_year = results[2]["year"]
        return question(f"There were {aResults} results for the movie, {originalMovie}. Here are the top 3. 1. {movie1} from {movie1_year}, 2. {movie2} from {movie2_year}, and 3. {movie3} from {movie3_year}. You can say, 1, 2, 3, or next page")
    elif mediaType == "series":
        originalSeries = session.attributes["series"]
        aResults = session.attributes["aResults"]
        results = session.attributes["results"]
        series1 = results[0]["title"]
        series1_year = results[0]["year"]
        series2 = results[1]["title"]
        series2_year = results[1]["year"]
        series3 = results[2]["title"]
        series3_year = results[2]["year"]
        return question(f"There were {aResults} results for the series, {originalSeries}. Here are the top 3. {series1} from {series1_year}, {series2} from {series2_year}, and {series3} from {series3_year}. You can say, 1, 2, 3, or next page")
    else:
        pass


# ! This still needs to be finished. MAybeby increminting the keys?
@ask.intent("NextPage")
def nextPage():
    mediaType = session.attributes["mediaType"]
    results = session.attributes["results"]

    try:
        plogic = session.attributes["plogic"]
        page = session.attributes["page"]
        session.attributes["plogic"] = plogic + 3
        session.attributes["page"] = page + 1
        plogic = plogic + 3
        page = page + 1



        n1 = 0 + plogic
        n2 = 1 + plogic
        n3 = 2 + plogic
    except KeyError:
        plogic = 3
        page = 2

        n1 = 0 + plogic
        n2 = 1 + plogic
        n3 = 2 + plogic

    if mediaType == "movie":
        try:
            movie1 = results[n1]["title"]
            movie1_year = results[n1]["year"]
            movie2 = results[n2]["title"]
            movie2_year = results[n2]["year"]
            movie3 = results[n3]["title"]
            movie3_year = results[n3]["year"]


            return question(f"Page {page}: 1. {movie1} from {movie1_year}, 2. {movie2} from {movie2_year}, and 3. {movie3} from {movie3_year}. You can say, 1, 2, 3, next page, or previous page")
        except:
            try:
                movie1 = results[n1]["title"]
                movie1_year = results[n1]["year"]
                movie2 = results[n2]["title"]
                movie2_year = results[n2]["year"]


                return question(f"Page {page}: This is the last page. 1. {movie1} from {movie1_year}, and 2. {movie2} from {movie2_year}. You can say, 1, 2, or previous page")
            except:
                try:
                    movie1 = results[n1]["title"]
                    movie1_year = results[n1]["year"]


                    return question(f"Page {page}: This is the last page. 1. {movie1} from {movie1_year}. You can say, 1, or previous page")
                except:
                    return question("There are no more results. Say previous page to go back")

    elif mediaType == "series":
        try:
            series1 = results[n1]["title"]
            series1_year = results[n1]["year"]
            series2 = results[n2]["title"]
            series2_year = results[n2]["year"]
            series3 = results[n3]["title"]
            series3_year = results[n3]["year"]

            return question(f"Page {page}: 1. {series1} from {series1_year}, 2. {series2} from {series2_year}, and 3. {series3} from {series3_year}. You can say, 1, 2, 3, next page, or previous page")
        except:
            try:
                series1 = results[n1]["title"]
                series1_year = results[n1]["year"]
                series2 = results[n2]["title"]
                series2_year = results[n2]["year"]

                return question(f"Page {page}: This is the last page. 1. {series1} from {series1_year}, and 2. {series2} from {series2_year}. You can say, 1, 2, or previous page")
            except:
                try:
                    series1 = results[n1]["title"]
                    series1_year = results[n1]["year"]


                    return question(f"Page {page}: This is the last page. 1. {series1} from {series1_year}. You can say, 1, or previous page")
                except:
                    return question("There are no more results. Say previous page to go back")

        else:
            pass



# ! This still needs to be finished. MAybeby increminting the keys?
@ask.intent("BackPage")
def backPage():
    mediaType = session.attributes["mediaType"]
    results = session.attributes["results"]

    try:
        plogic = session.attributes["plogic"]
        page = session.attributes["page"]

        session.attributes["plogic"] = plogic - 3
        session.attributes["page"] = page - 1

        plogic = plogic - 3
        page = page - 1

        n1 = 0 + plogic
        n2 = 1 + plogic
        n3 = 2 + plogic
    except:
        return question("That didnt work how it was supposed to")

    if mediaType == "movie":
        try:
            movie1 = results[n1]["title"]
            movie1_year = results[n1]["year"]
            movie2 = results[n2]["title"]
            movie2_year = results[n2]["year"]
            movie3 = results[n3]["title"]
            movie3_year = results[n3]["year"]


            return question(f"Page {page}: 1. {movie1} from {movie1_year}, 2. {movie2} from {movie2_year}, and 3. {movie3} from {movie3_year}. You can say, 1, 2, 3, next page, or previous page")
        except:
            try:
                movie1 = results[n1]["title"]
                movie1_year = results[n1]["year"]
                movie2 = results[n2]["title"]
                movie2_year = results[n2]["year"]


                return question(f"Page {page}: This is the last page. 1. {movie1} from {movie1_year}, and 2. {movie2} from {movie2_year}. You can say, 1, 2, or previous page")
            except:
                try:
                    movie1 = results[n1]["title"]
                    movie1_year = results[n1]["year"]


                    return question(f"Page {page}: This is the last page. 1. {movie1} from {movie1_year}. You can say, 1, or previous page")
                except:
                    return question("There are no more results. Say previous page to go back")

    elif mediaType == "series":
        try:
            series1 = results[n1]["title"]
            series1_year = results[n1]["year"]
            series2 = results[n2]["title"]
            series2_year = results[n2]["year"]
            series3 = results[n3]["title"]
            series3_year = results[n3]["year"]

            return question(f"Page {page}: 1. {series1} from {series1_year}, 2. {series2} from {series2_year}, and 3. {series3} from {series3_year}. You can say, 1, 2, 3, next page, or previous page")
        except:
            try:
                series1 = results[n1]["title"]
                series1_year = results[n1]["year"]
                series2 = results[n2]["title"]
                series2_year = results[n2]["year"]

                return question(f"Page {page}: This is the last page. 1. {series1} from {series1_year}, and 2. {series2} from {series2_year}. You can say, 1, 2, or previous page")
            except:
                try:
                    series1 = results[n1]["title"]
                    series1_year = results[n1]["year"]

                    return question(f"Page {page}: This is the last page. 1. {series1} from {series1_year}. You can say, 1, or previous page")
                except:
                    return question("There are no more results. Say previous page to go back")

        else:
            pass


@ask.intent("ChoiceOne")
def choiceOne():
    mediaType = session.attributes["mediaType"]
    results = session.attributes["results"]
    plogic = session.attributes["plogic"]
    n1 = 0 + plogic

    if mediaType == "movie":
        movieName = results[n1]["title"]
        year = results[n1]["year"]
        tmdbId = results[n1]["tmdbId"]
        # * Add movie/series and get status code
        status = addMovie(tmdbId, radarr_api, radarr_profile, radarr_monitored, radarr_autosearch, radarr_url)
        # Check the status code and return the appropriate response
        if status == 400:
            return statement(f"The movie {movieName}, from {year}, has already been added to Radar.")
        elif status == 201:
            return statement(f"I added the movie, {movieName}, from {year}, to Radarr")
        elif status == 404:
            return statement("I was unable to communicate with Radarr. Check your settings and make sure the server is up")
        else:
            return statement("Something out of my control went wrong")

    else:
        seriesName = results[n1]["title"]
        year = results[n1]["year"]
        tvdbId = results[n1]["tvdbId"]
        # * Add movie/series and get status code
        status = addSeries(tvdbId, sonarrAPI, sonarr_profile, sonarr_monitored, sonarr_autosearch, sonarr_seriesType, sonarr_seasonfolder, sonarr_url)
        # Check the status code and return the appropriate response
        if status == 400:
            return statement(f"The series {seriesName}, from {year}, has already been added to Sonarr.")
        elif status == 201:
            return statement(f"I added the series, {seriesName}, from {year}, to Sonarr")
        elif status == 404:
            return statement("I was unable to communicate with Sonarr. Check your settings and make sure the server is up")
        else:
            return statement("Something out of my control went wrong")


@ask.intent("ChoiceTwo")
def choiceTwo():
    mediaType = session.attributes["mediaType"]
    results = session.attributes["results"]
    plogic = session.attributes["plogic"]
    n2 = 1 + plogic

    if mediaType == "movie":
        movieName = results[n2]["title"]
        year = results[n2]["year"]
        tmdbId = results[n2]["tmdbId"]
        # * Add movie/series and get status code
        status = addMovie(tmdbId, radarr_api, radarr_profile, radarr_monitored, radarr_autosearch, radarr_url)
        # Check the status code and return the appropriate response
        if status == 400:
            return statement(f"The movie {movieName}, from {year}, has already been added to Radar.")
        elif status == 201:
            return statement(f"I added the movie, {movieName}, from {year}, to Radarr")
        elif status == 404:
            return statement("I was unable to communicate with Radarr. Check your settings and make sure the server is up")
        else:
            return statement("Something out of my control went wrong")

    else:
        seriesName = results[n2]["title"]
        year = results[n2]["year"]
        tvdbId = results[n2]["tvdbId"]
        # * Add movie/series and get status code
        status = addSeries(tvdbId, sonarrAPI, sonarr_profile, sonarr_monitored, sonarr_autosearch, sonarr_seriesType, sonarr_seasonfolder, sonarr_url)
        # Check the status code and return the appropriate response
        if status == 400:
            return statement(f"The series {seriesName}, from {year}, has already been added to Sonarr.")
        elif status == 201:
            return statement(f"I added the series, {seriesName}, from {year}, to Sonarr")
        elif status == 404:
            return statement("I was unable to communicate with Sonarr. Check your settings and make sure the server is up")
        else:
            return statement("Something out of my control went wrong")


@ask.intent("ChoiceThree")
def choiceThree():
    mediaType = session.attributes["mediaType"]
    results = session.attributes["results"]
    plogic = session.attributes["plogic"]
    n3 = 2 + plogic

    if mediaType == "movie":
        movieName = results[n3]["title"]
        year = results[n3]["year"]
        tmdbId = results[n3]["tmdbId"]
        # * Add movie/series and get status code
        status = addMovie(tmdbId, radarr_api, radarr_profile, radarr_monitored, radarr_autosearch, radarr_url)
        # Check the status code and return the appropriate response
        if status == 400:
            return statement(f"The movie {movieName}, from {year}, has already been added to Radar.")
        elif status == 201:
            return statement(f"I added the movie, {movieName}, from {year}, to Radarr")
        elif status == 404:
            return statement("I was unable to communicate with Radarr. Check your settings and make sure the server is up")
        else:
            return statement("Something out of my control went wrong")

    else:
        seriesName = results[n3]["title"]
        year = results[n3]["year"]
        tvdbId = results[n3]["tvdbId"]
        # * Add movie/series and get status code
        status = addSeries(tvdbId, sonarrAPI, sonarr_profile, sonarr_monitored, sonarr_autosearch, sonarr_seriesType, sonarr_seasonfolder, sonarr_url)
        # Check the status code and return the appropriate response
        if status == 400:
            return statement(f"The series {seriesName}, from {year}, has already been added to Sonarr.")
        elif status == 201:
            return statement(f"I added the series, {seriesName}, from {year}, to Sonarr")
        elif status == 404:
            return statement("I was unable to communicate with Sonarr. Check your settings and make sure the server is up")
        else:
            return statement("Something out of my control went wrong")


@ask.intent("addAll")
def addAll():
    try:
        results = session.attributes["results"]
        movie1 = results[0]["title"]
        movie1id = results[0]["tmdbId"]
        movie2 = results[1]["title"]
        movie2id = results[1]["tmdbId"]
        movie3 = results[2]["title"]
        movie3id = results[2]["tmdbId"]

        status1 = addMovie(movie1id, radarr_api, radarr_profile,
                           radarr_monitored, radarr_autosearch, radarr_url)
        status2 = addMovie(movie2id, radarr_api, radarr_profile,
                           radarr_monitored, radarr_autosearch, radarr_url)
        status3 = addMovie(movie3id, radarr_api, radarr_profile,
                           radarr_monitored, radarr_autosearch, radarr_url)

        return statement(f"I added the movies {movie1}, {movie2} and {movie3} to Radar")
    except KeyError:
        try:
            results = session.attributes["results"]
            movie1 = results[0]["title"]
            movie1id = results[0]["tmdbId"]
            movie2 = results[1]["title"]
            movie2id = results[1]["tmdbId"]

            status1 = addMovie(movie1id, radarr_api, radarr_profile,
                               radarr_monitored, radarr_autosearch, radarr_url)
            status2 = addMovie(movie2id, radarr_api, radarr_profile,
                               radarr_monitored, radarr_autosearch, radarr_url)

            return statement(f"I added the movies {movie1} and {movie2} to Radar")
        except KeyError:
            results = session.attributes["results"]
            movie1 = results[0]["title"]
            movie1id = results[0]["tmdbId"]

            status1 = addMovie(movie1id, radarr_api, radarr_profile,
                               radarr_monitored, radarr_autosearch, radarr_url)

            return statement(f"I added the movie {movie1} to Radar")


@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    print("alexa-subwatch up and running!")
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    #app.run("0.0.0.0", 5000, debug=False)
