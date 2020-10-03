import geopy
import geopy.distance
import googlemaps
import pandas as pd
import pickle
import numpy as np
import os
import lightgbm as lgb


def save_obj(obj, name):
    with open('./' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def get_nearby_places(latitude: int, longitude: int, api_key: str, place_type: str, radius: int = 1000):
    gmaps = googlemaps.Client(key=api_key)
    places_result = gmaps.places_nearby(location=f"{latitude}, {longitude}", radius=radius,
                                        type=place_type)
    if places_result['status'] == 'ZERO_RESULTS':
        return -1
    return places_result['results']


def extract_data(data_df, extr_data):
    merge_col = extr_data.columns[1]
    data_df = pd.merge(data_df, extr_data, on='id')
    data_df[f'dist_to_{merge_col}'] = (np.zeros_like(data_df['id']) - 1).astype(np.float64)
    data_df[f'nearest_{merge_col}'] = (np.zeros_like(data_df['id']) - 1).astype(np.float64)
    data_df[f'nearest_{merge_col}_rating'] = (np.zeros_like(data_df['id']) - 1).astype(np.float64)
    data_df[f'nearest_{merge_col}_num_ratings'] = (np.zeros_like(data_df['id']) - 1).astype(np.int64)
    data_df[f'num_{merge_col}_around'] = np.zeros_like(data_df['id'])
    data_df[f'{merge_col}_locations'] = np.zeros_like(data_df['id']) - 1
    for i in range(len(data_df)):
        if data_df[merge_col][i] != -1:
            data_df[f'num_{merge_col}_around'][i] = len(data_df[merge_col][i])
            coordinates_of_malls = []
            for j in range(len(data_df[merge_col][i])):
                mall_location = data_df[merge_col][i][j]['geometry']['location']
                coordinates_of_malls.append(mall_location)
            data_df[f'{merge_col}_locations'][i] = coordinates_of_malls

    for i in range(len(data_df[merge_col])):
        if data_df[merge_col][i] != -1:
            distances = []
            for j in range(len(data_df[f'{merge_col}_locations'][i])):
                coord1 = (data_df['latitude'][i], data_df['longitude'][i])
                coord2 = (
                    data_df[f'{merge_col}_locations'][i][j]['lat'], data_df[f'{merge_col}_locations'][i][j]['lng'])
                distance = geopy.distance.geodesic(coord1, coord2).km
                distances.append(distance)
            data_df[f'nearest_{merge_col}'][i] = np.argmin(distances)
            data_df[f'dist_to_{merge_col}'][i] = np.min(distances)
            try:
                data_df[f'nearest_{merge_col}_rating'][i] = data_df[merge_col][i][(np.argmin(distances))]['rating']
                data_df[f'nearest_{merge_col}_num_ratings'][i] = data_df[merge_col][i][(np.argmin(distances))][
                    'user_ratings_total']
            except:
                pass
    return data_df


def run_prediction(LAT: int, LONG: int, KEY: str):
    FEATURES = ['num_church_around',
                'nearest_church_num_ratings',
                'nearest_church_rating',
                'dist_to_church',
                'num_bus_station_around',
                'nearest_bus_station_num_ratings',
                'nearest_bus_station_rating',
                'nearest_bus_station',
                'dist_to_bus_station',
                'num_parking_around',
                'nearest_parking_num_ratings',
                'nearest_parking_rating',
                'dist_to_parking',
                'num_university_around',
                'nearest_university_num_ratings',
                'nearest_university_rating',
                'dist_to_university'
                ]
    shopping_mall = get_nearby_places(LAT, LONG, KEY, 'shopping_mall')
    university = get_nearby_places(LAT, LONG, KEY, 'university')
    church = get_nearby_places(LAT, LONG, KEY, 'church')
    bus_station = get_nearby_places(LAT, LONG, KEY, 'bus_station')
    parking = get_nearby_places(LAT, LONG, KEY, 'parking')
    coordinates = pd.DataFrame()
    coordinates['latitude'] = [LAT]
    coordinates['longitude'] = [LONG]
    coordinates['id'] = [0]
    a = pd.concat([coordinates, coordinates])
    for (places_result, colname) in list(zip([shopping_mall, church, university, bus_station, parking],
                                             ['shopping_mall', 'church', 'university', 'bus_station', 'parking'])):
        result = pd.DataFrame()
        result['id'] = [0]
        result[colname] = [places_result]
        b = pd.concat([result, result])
        a = extract_data(a, b)
    print(os.getcwd())
    model = load_obj('./model.pkl')

    predict = model.predict(a[FEATURES])[0]
    return predict
