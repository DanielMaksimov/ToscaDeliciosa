import requests
import requests_oauthlib
import os
import json
import searchtweets as st
import urllib.parse
import credentials
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

consumer_key = credentials.consumer_key
consumer_secret = credentials.consumer_secret
access_key = credentials.access_key
access_secret = credentials.access_secret
bearer_token = credentials.bearer_token


def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    # usernames = "usernames=elonmusk"
    # user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    #BRAZIL query = "place_country:BR -is:retweet"
    #query = "point_radius:[-47.955842 -15.832497 20km] place_country:BR" #CAREFUL LONGITUDE LATITUDE
    #query = "point_radius:[3.878045 43.609100 10km] place_country:FR"
    query = "place:\"rio de janeiro\" place_country:BR"
    # Number of tweets from Brazil in the last month
    # url = "https://api.twitter.com/2/tweets/counts/all?query=" + urllib.parse.quote(query) + "&granularity=day&start_time=" + urllib.parse.quote("2022-04-01T00:00:01.000Z")
    # .format(usernames, user_fields)
    url = "https://api.twitter.com/2/tweets/counts/all?query=" + urllib.parse.quote(query) + "&granularity=day&start_time=" + urllib.parse.quote("2022-04-01T00:00:01.000Z")
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "TipTopTundra"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth,)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main1():
    base_url = create_url()
    json_response = connect_to_endpoint(base_url)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    total_nb = 0
    x, y = [], []

    for i in range(len(json_response["data"])):
        y.append(json_response["data"][i]["tweet_count"])
        x.append(i)

    while 'next_token' in json_response['meta']:
        total_nb += json_response['meta']['total_tweet_count']
        pag_token = json_response['meta']['next_token']
        url = base_url + "&pagination_token=" + pag_token
        json_response = connect_to_endpoint(url)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        for i in range(len(json_response["data"])):
            y.append(json_response["data"][i]["tweet_count"])
            x.append(x[-1] + 1)

    print("Total number of tweets: " + str(total_nb))

    plt.plot(x, y)
    plt.show()


def city_data(city: str, country: str, start_date: str):
    # The query made to get info on our city
    base_url = "https://api.twitter.com/2/tweets/counts/all?query=" + \
               urllib.parse.quote("place:" + city + " place_country:" + country) + \
               "&granularity=day&start_time=" + \
               urllib.parse.quote(start_date + "T00:00:01.000Z")

    # Sending the query
    json_response = connect_to_endpoint(base_url)
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    total_nb = 0
    dic = {}

    for i in range(len(json_response["data"])):
        dic[json_response["data"][i]["start"]] = json_response["data"][i]["tweet_count"]

    while 'next_token' in json_response['meta']:
        total_nb += json_response['meta']['total_tweet_count']
        pag_token = json_response['meta']['next_token']
        url = base_url + "&pagination_token=" + pag_token
        json_response = connect_to_endpoint(url)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        for j in range(len(json_response["data"])):
            dic[json_response["data"][j]["start"]] = json_response["data"][j]["tweet_count"]

    print("Total number of tweets: " + str(total_nb))

    ord_dict = dict(sorted(dic.items()))
    x, y = [], []
    for i in ord_dict.keys():
        x.append(i[:10])
        y.append(ord_dict[i])
    plt.plot(x, y)
    plt.xticks(rotation=50)
    plt.show()


def bounding_box_data(bounding_box: [int], start_date: str):
    # The query made to get info on our city
    base_url = "https://api.twitter.com/2/tweets/search/all?query=" + \
               urllib.parse.quote("bounding_box:" + str(bounding_box).replace(',', '')) + \
               " -is:retweet&tweet.fields=geo&start_time=" + \
               urllib.parse.quote(start_date + "T00:00:01.000Z") + \
               "&max_results=500"
    store = pd.HDFStore("/home/maksimov/ToscaDeliciosa/data/HDFStore_Twitter_Rio_2.hdf5")

    # Sending the query
    json_response = connect_to_endpoint(base_url)
    # Extracting data
    while 'next_token' in json_response['meta']:
        time.sleep(2)
        coordinates_list = []
        # print(json.dumps(json_response, indent=4, sort_keys=True))
        for i in range(len(json_response["data"])):
            if "coordinates" in json_response["data"][i]["geo"] and \
                    json_response["data"][i]["geo"]["coordinates"]["type"] == "Point":
                coordinates = json_response["data"][i]["geo"]["coordinates"]["coordinates"]
                coordinates_list.append(coordinates)
        # Converting to dataframe and adding to store
        page_df = pd.DataFrame(coordinates_list, columns=['lon', 'lat'])
        store.append('data_geo', page_df, format='t')
        # Saving the page
        pag_token = json_response['meta']['next_token']
        df_pag_token = pd.DataFrame([[pag_token]], columns=['next_pag_token'])
        store.append('data_pag', df_pag_token, format='t')

        # Building the next query
        url = base_url + "&pagination_token=" + pag_token
        json_response = connect_to_endpoint(url)

    # Last page
    for i in range(len(json_response["data"])):
        coordinates_list = []
        if "coordinates" in json_response["data"][i]["geo"] and \
                json_response["data"][i]["geo"]["coordinates"]["type"] == "Point":
            coordinates = json_response["data"][i]["geo"]["coordinates"]["coordinates"]
            coordinates_list.append(coordinates)
    page_df = pd.DataFrame(coordinates_list, columns=['lon', 'lat'])
    store.append('data_geo', page_df, format='t')
    # print(json.dumps(json_response, indent=4, sort_keys=True))
    store.close()

    """
    for i in range(len(json_response["data"])):
        dic[json_response["data"][i]["start"]] = json_response["data"][i]["tweet_count"]

    while 'next_token' in json_response['meta']:
        total_nb += json_response['meta']['total_tweet_count']
        pag_token = json_response['meta']['next_token']
        url = base_url + "&pagination_token=" + pag_token
        json_response = connect_to_endpoint(url)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        for j in range(len(json_response["data"])):
            dic[json_response["data"][j]["start"]] = json_response["data"][j]["tweet_count"]

    """
    return 0


def create_geo_array(x_min, x_max, y_min, y_max, nb_points):
    x = np.linspace(x_min, x_max, nb_points)
    y = np.linspace(y_min, y_max, nb_points)
    mat = np.zeros((nb_points, nb_points))
    return x, y, mat


def fill_geo_array(mat, x, y, coordinates):
    """Returns a grid array with each value representing the number of points in that square"""
    mat_copy = np.copy(mat)
    for point in coordinates:
        lon, lat = point[0], point[1]
        i, j = 1, 1
        while lon > x[i] and i < len(x) - 1:
            i += 1
        while lat > y[j] and j < len(y) - 1:
            j += 1
        mat[j-1][i-1] += 1
    return mat_copy


if __name__ == "__main__":
    bbox = np.array([-43.419633, -23.008085, -43.147179, -22.833099])
    bounding_box_data(bbox, "2022-05-02")
