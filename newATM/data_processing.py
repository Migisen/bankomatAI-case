import os

import herepy
import pandas as pd
import googlemaps
from matplotlib import pyplot as plt
import requests
from .models import Atm


def get_info(model_list: list, img_name=None):
    df = pd.DataFrame(model_list.values())
    coordinates = [(long, lat) for long, lat in zip(df.longitude, df.latitude)]
    if img_name is None:
        get_image(coordinates)
    else:
        get_image(coordinates, img_name)


def get_multiple_info(df):
    coordinates = [(long, lat) for long, lat in zip(df.long, df.lat)]
    get_image(coordinates, img_name='mappred.png', z=20)


def get_image(coordinates, img_name='maps.png', z=13) -> None:
    api_key = 'Z1KAtxmnqH87jAHTrHtJzh3W6v_v7Oij6ns2tw_qejQ'
    url = 'https://image.maps.ls.hereapi.com/mia/1.6/'
    s = requests.Session()
    request_params = {
        'apiKey': api_key,
        'z': z,
        'ml': 'rus',
        'ppi': 520,
        'poi': '',
        'w': 856
    }
    for n, coordinate_pair in enumerate(coordinates):
        request_params['poi'] += f'{coordinate_pair[1]},{coordinate_pair[0]},'

    response = s.get(url, params=request_params)
    print(response.url)
    with open(f'C:\\Users\\Migisen\\PycharmProjects\\gazpromProject\\newATM\\static\\maps\\{img_name}', 'wb') as f:
        f.write(response.content)
