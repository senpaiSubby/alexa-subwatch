#!/usr/bin/env python
# _____  _              _       _____       _    _  _
# |   __||_| _____  ___ | | _ _ |   __| _ _ | |_ | ||_| _____  ___
# |__   || ||     || . || || | ||__   || | || . || || ||     || -_|
# |_____||_||_|_|_||  _||_||_  ||_____||___||___||_||_||_|_|_||___|
#                 |_|     |___|

import requests

def requestSeries():
    pass


def requestMovie():

    post_data = {
        "user": user,
        "theMovieDbId": tmdbId,
        "languageCode": language,
    },
    headers = {
        "Content-Type": "application/json",
        "ApiKey": API,
    },

    status = requests.post(
        url, json=post_data, headers=headers)
    return (status)

print(requestMovie())
