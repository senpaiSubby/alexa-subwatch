#!/usr/bin/env python
# _____  _              _       _____       _    _  _
# |   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
# |__   || ||     || . || || | ||__   || | || . || || ||     || -_|
# |_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|
import requests
import json


def searchSeries(searchTerm, apiKey, url, sortingMode):
    """Searchs for series via string.

    Arguments:
        searchterm {str} -- Series to search for.
        apiKey {int} -- Sonarr's API key.
        url {str} -- Sonarr's web url.

    Returns:
        [list] -- Returns a list dictionaties containing the resulting series
        matches after being ran through duplicates()
    """
    searchTerm = searchTerm.replace(" ", "%20")
    sonarr = requests.get(url + "/api/series/lookup/?term=" +
                          searchTerm + "&apikey=" + str(apiKey))
    results = sonarr.json()

    return duplicates(results, sortingMode)

def sonarrTest(url):
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
            "tvdbId": i["tvdbId"],
            "rating": i["ratings"]["value"],
        },)


    results = sorted(results, key=lambda k: k[sortingMode], reverse=True)
    #x = json.dumps(results, indent=4)
    #print(x)



    return results

#searchSeries("smallville", "981298f8bc1d4267b8826cc22b3e425d", "https://sonarr.atriox.io", "year")

def addSeries(tvdbId, apiKey, profile, monitored, autosearch, seriesType, seasonfolder, url):
    """Adds a series to Sonarr via its tvdbId number

    Arguments:
        tvdbId {int} -- The TVDB ID of the series to add.
        apiKey {str} -- Sonarr's API key.
        profile {int} -- The quality profile number.
        monitored {boolean} -- Whether or not monitor the series after adding.
        autosearch {boolean} -- Whether or not to automatically search for series after.
        seriesType {boolean} -- Is the series Anime or normal.
        seasonfolder {boolean} -- Whether or not to keep series in a season folder.
        url {str} -- Sonarr's URL including the https/http
    """
    result = requests.get(url + "/api/series/lookup?term=tvdbId:" +
                          str(tvdbId) + "&apikey=" + str(apiKey))
    result = result.json()

    post_data = {
        "qualityProfileId": profile,
        "rootFolderPath": "/data/media/tv/series/",
        "seriesType": seriesType,
        "monitored": monitored,
        "seasonFolder": seasonfolder,
        "addOptions": {"searchForMissingEpisodes": autosearch},
    }

    for dictkey in ["tvdbId", "title", "titleSlug", "images", "year", "seasons"]:
        post_data.update({dictkey: result[0][dictkey]})

    status = requests.post(url + "/api/series?apikey=" +
                           str(apiKey), json=post_data)
    status = status.status_code

    """
    400 = exists
    201 = added
    404 = no route
    """
    return status
