import os

import herepy
import pandas as pd
import googlemaps
from matplotlib import pyplot as plt
import requests
from .models import Atm


def get_info(model_list: list, key: str):
    df = pd.DataFrame(model_list.values())
    coordinates = [(long, lat) for long, lat in zip(df.longitude, df.latitude)]
    get_image(coordinates)


def get_image(coordinates) -> None:
    api_key = 'Z1KAtxmnqH87jAHTrHtJzh3W6v_v7Oij6ns2tw_qejQ'
    url = 'https://image.maps.ls.hereapi.com/mia/1.6/stat'
    s = requests.Session()
    request_params = {
        'apiKey': api_key
    }
    for n, coordinate_pair in enumerate(coordinates):
        request_params[f'o{n}'] = str(coordinate_pair) + ';10'
    response = s.get(url, params=request_params)

    with open('C:\\Users\\Migisen\\PycharmProjects\\gazpromProject\\newATM\\static\\maps\\maps.png', 'wb') as f:
        f.write(response.content)


