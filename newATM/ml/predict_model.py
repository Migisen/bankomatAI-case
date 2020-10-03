import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.datasets import make_regression
import pickle


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)


def generate_near_points(lat, long):
    num_points = np.random.randint(15) + 1
    df = pd.DataFrame()
    df['lat'] = np.zeros(num_points) + np.random.uniform(low=0.0, high=.0002, size=num_points ) + lat
    df['long'] = np.zeros(num_points) + np.random.uniform(low=0.0, high=.0002, size=num_points) + long
    features, _ = make_regression(n_samples=num_points, n_features=17, random_state=42)
    return df.join(pd.DataFrame(features))


def run_prediction(lat, long):
    model = load_obj('C:\\Users\\Migisen\\PycharmProjects\\gazpromProject\\newATM\\model.pkl')
    datka = generate_near_points(lat, long)
    datka['predict'] = model.predict(datka)
    return datka[['lat', 'long', 'predict']]


run_prediction(0, 0)
