#!/usr/bin/env python
# _____  _              _       _____       _    _  _
# |   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
# |__   || ||     || . || || | ||__   || | || . || || ||     || -_|
# |_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|
import requests
import json


def searchMovie(searchterm, apiKey, url, sortingMode):
    """Searchs for movie via string and return a list dictionaties containing the resulting movie
        matches after being ran through duplicates()

    Arguments:
        searchterm {str} -- Movie to search for.
        apiKey {int} -- Radarr's API key.
        url {str} -- Radarr's web url.

    Returns:
        [list] -- Returns a list dictionaties containing the resulting movie
        matches after being ran through duplicates()
    """
    # Replace spaces from search term
    searchterm = searchterm.replace(" ", "%20")
    # Makes API request and return data
    radarr = requests.get(url + "/api/movie/lookup/?term=" +
                          searchterm + "&apikey=" + str(apiKey))
    results = radarr.json()

    return duplicates(results, sortingMode)


def radarrTest(url):
    try:
        requests.get(url + "/api")
        return(True)
    except requests.exceptions.RequestException as e:
        print(e)
        return(False)


def duplicates(results_json, sortingMode):
    results = []

    for i in results_json:
        results.append({
            "title": i["title"],
            "year": i["year"],
            "tmdbId": i["tmdbId"],
            "rating": i["ratings"]["value"],
            "poster": i["remotePoster"],
        },)


    results = sorted(results, key=lambda k: k[sortingMode], reverse=True)
    #x = json.dumps(results, indent=4)
    #print(x)
    return results


#searchMovie("Black Hawk Down", "22833f986d5543ce94ea197a1d21dfb8", "https://radarr.atriox.io", "rating")




def addMovie(tmdbId, apiKey, profile, monitored, autosearch, url):
    """Adds a series to Sonarr via its tvdbId number.

    Arguments:
        tmdbId {int} -- The tmdbId ID of the movie to add.
        apiKey {str} -- Radarr's API key.
        profile {int} -- The quality profile number.
        monitored {boolean} -- Whether or not monitor the movie after adding.
        autosearch {boolean} -- Whether or not to automatically search for movie after.
        url {str} -- Radarr's URL including the https/http
    """

    result = requests.get(url + "/api/movie/lookup/tmdb?tmdbId=" +
                          str(tmdbId) + "&apikey=" + str(apiKey))
    result = result.json()

    post_data = {
        "qualityProfileId": profile,
        "rootFolderPath": "/data/media/movies/",
        "monitored": monitored,
        "addOptions": {"searchForMovie": autosearch},
    }

    for dictkey in ["tmdbId", "title", "titleSlug", "images", "year"]:
        post_data.update({dictkey: result[dictkey]})

    status = requests.post(url + "/api/movie?apikey=" +
                           str(apiKey), json=post_data)
    status = status.status_code

    """
    400 = exists
    201 = added
    404 = no route
    """
    return status
