#!/usr/bin/env python3
"""
    Trading Bot for cryptocurrency
"""
import sys
from binance.client import Client
from BinanceKeys import api_key, api_secret
from tBotFunctions import getdata, indicators
from tBotHelperFunctions import *
from tBotBuySell import buy, sell, checkbuy, checksell
import time

client = Client(api_key, api_secret)
symbol = str(sys.argv[1]).upper()
investment = int(sys.argv[2])

while True:
    df = indicators(getdata(client, symbol))
    if checkbuy(df, investment):
        curr_order = buy(client, investment)

    try:
        checksell(client, df, curr_order)

    except:
        print('Not an order yet')
    time.sleep(60)
