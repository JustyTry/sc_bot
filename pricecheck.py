import requests
import pandas
import os
import json
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv('URL_AUCTION')
TOKEN = os.getenv('USER_TOKEN')

limit = 32

headers = {'Authorization': f'Bearer {TOKEN}',
           'Content-Type': 'application/json'}

# Запрос истории предмета
percentage = 5


def makePriceHistoryRequest(id):
    res = requests.get(
        f"{URL}/{id}/history?limit={limit}&additional=true", headers=headers)
    data = res.json()
    averagesum = 0
    prices = data["prices"]
    medianvalues = []
    if len(prices):
        for el in prices:
            averagesum = averagesum + int(el["price"]) // limit
            medianvalues.append(int(el["price"]))
        median = 0
        if len(medianvalues) % 2:
            median = medianvalues[len(medianvalues) // 2]
        else:
            median = medianvalues[len(medianvalues) // 2] + \
                medianvalues[len(medianvalues) // 2 + 1]
            median = median // 2
    return [averagesum, median]

# Запрос текущих лотов предмета


def makeCurrentPriceRequest(id):
    res = requests.get(
        f"{URL}/{id}/lots", headers=headers)
    data = res.json()
    poses = []
    
    for el in data["lots"]:
        poses.append(el["buyoutPrice"] // el["amount"])

    return poses

# сравнение со средней ценой и поиск выгоды 5+%


def comparePrice(id):
    lots = []
    averagepricehistory = makePriceHistoryRequest(id)[0]
    averageprice = averagepricehistory - \
        ((averagepricehistory // 100) * percentage)
    for price in makeCurrentPriceRequest(id):
        if price <= averageprice and price != 0:
            lots.append(price)
        else:
            continue
    if len(lots):
        return [lots, averagepricehistory, makePriceHistoryRequest(id)[1]]
    return 0
