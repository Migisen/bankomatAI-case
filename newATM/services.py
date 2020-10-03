import requests


from .models import Atm
import pickle
from django.core import serializers


# Если получать респонсы через API, пока просто загружаем в бд
def get_atms(url: str = 'https://www.gazprombank.ru/rest/hackathon/atm/?page=') -> list:
    response: list = []
    atm_models = []
    for page in range(1, 3):
        cur_url: str = url + str(page)
        response += requests.get(cur_url).json()
    for atm in response:
        atm_model = {
            'pk': atm['id'],
            'model': 'newATM.Atm',
            'fields': {
                'id': atm['id'],
                'latitude': atm['geolocation']['latitude'],
                'longitude': atm['geolocation']['longitude'],
                'region': atm['address']['region'],
                'region_type': atm['address']['regionType'],
                'settlement_type': atm['address']['settlementType'],
                'settlement': atm['address']['settlement'],
                'location': atm['address']['location'],
                'full_address': atm['address']['fullAddress'],
            }
        }
        atm_models.append(atm_model)
        with open('atms.pkl', 'wb') as f:
            pickle.dump(atm_models, f)
    return response


