import requests
import pandas
import os
from dotenv import load_dotenv


load_dotenv()
URL = os.getenv('URL_EMISSION')
TOKEN = os.getenv('USER_TOKEN')

headers = {'Authorization': f'Bearer {TOKEN}',
           'Content-Type': 'application/json'}


def makeEmissonRequest():
    res = requests.get(URL, headers=headers)
    data = res.json()
    return data


def compareTime():

    if "currentStart" in makeEmissonRequest():
        return True
    else:
        return False
