import requests
import json
import datetime
import random

BASE = "RUB"

def data_parse(data_string):
    data = datetime.datetime.strptime(data_string, r"%Y-%m-%d")
    return data.strftime(r"%d.%m.%Y")

def get_usd(nvalue = None):
    data = requests.get("https://api.exchangeratesapi.io/latest?base=USD&symbols=RUB")
    jdata = json.loads(data.text)
    value, data = float(jdata.get("rates").get("RUB")), jdata.get("date")
    if nvalue is None:
        ret_string = "По состоянию на {0}:\n1 USD = {1} RUB.{2}".format(data_parse(data), round(value, 2), "\nКрепитесь..." if random.randint(0, 5) < 1 else "")
    else:
        ret_string = "По состоянию на {0}:\n{3} USD = {1} RUB.{2}".format(data_parse(data), round(value * float(nvalue), 2), "\nКрепитесь..." if random.randint(0, 5) < 1 else "", nvalue)
    return ret_string

def get_eur(nvalue = None):
    data = requests.get("https://api.exchangeratesapi.io/latest?base=EUR&symbols=RUB")
    jdata = json.loads(data.text)
    value, data = float(jdata.get("rates").get("RUB")), jdata.get("date")
    if nvalue is None:
        ret_string = "По состоянию на {0}:\n1 EUR = {1} RUB.{2}".format(data_parse(data), round(value, 2), "\nКрепитесь..." if random.randint(0, 5) < 1 else "")
    else:
        ret_string = "По состоянию на {0}:\n{3} EUR = {1} RUB.{2}".format(data_parse(data), round(value * float(nvalue), 2), "\nКрепитесь..." if random.randint(0, 5) < 1 else "", nvalue)
    return ret_string



