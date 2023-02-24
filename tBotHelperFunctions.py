#!/usr/bin/python3
"""
    Helper functions to place a buy order
"""

def pricecalc(client, symbol, limit=0.97):
    """
        Determines the price to buy at
    """
    raw_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
    dec_len = len(str(raw_price).split('.')[1])
    price = raw_price * limit
    return round(price, dec_len)

def quantitycalc(client, symbol, investment):
    """
        Determines the quantity of cryptocurrency to buy
    """
    info = client.get_symbol_info(symbol=symbol)
    Lotsize = float([i for i in info['filters'] if
                    i['filterType'] == 'LOT_SIZE'][0]['minQty'])
    price = pricecalc(client, symbol)
    qty = round(investment/price, right_rounding(Lotsize))
    return qty

def right_rounding(Lotsize):
    splitted = str(Lotsize).split('.')
    if float(splitted[0]) == 1:
        return 0
    else:
        return len(splitted[1])