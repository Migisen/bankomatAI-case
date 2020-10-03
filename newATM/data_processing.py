import pandas as pd
import googlemaps
from matplotlib import pyplot as plt
from .models import Atm


def get_info(model_list: list, key: str):
    df = pd.DataFrame(model_list.values())
    places = ['atm']
    df.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4)
    plt.show()


def request_google(longitude: float, latitude: float, places: list, key: str):
    gmaps = googlemaps.Client(key=key)
    result = {}
    for place in places:
        places_result = gmaps.places_nearby(location=f'{latitude}, {longitude}', radius=1000, type=places)
        if places_result['status'] == 'ZERO_RESULT':
            result[place] = None
        else:
            result[place] = places_result['results']
    return result
