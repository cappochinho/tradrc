#!/usr/bin/env python3
import pandas as pd
from datetime import timedelta


pos_dict = {'in_position': False}
def buy(client, investment):
    order = client.order_limit_buy(symbol=symbol,
                                   price = pricecalc(client, symbol),
                                   quantity = quantitycalc(client, symbol, investment))
    
    print(order)
    pos_dict['in_position'] = True
    return order

def sell(client, qty):
    order = client.create_order(symbol=symbol,
                               side='SELL',
                               type='MARKET',
                               quantity=qty)
    
    print(order)
    pos_dict['in_position'] = False

def checkbuy(df, investment):
    if not pos_dict['in_position']:
        if df.Buy.values:
            return True
    else:
        print('already in a position')

def checksell(client, df, order):
    order_status = client.get_order(symbol=symbol, orderId=order['orderId'])
    if pos_dict['in_position']:
        if order_status['status'] == 'NEW':
            print('buy limit order pending')
        elif order_status['status'] == 'FILLED':
            cond1 = df.Close.values > float(order_status['price'])
            cond2 = pd.to_datetime('now') >= pd.to_datetime(
                    order_status['updateTime'], unit='ms') + timedelta(minutes=150)

            if cond1 or cond2:
                sell(client, order_status['origQty'])
    
    else:
        print('currently not in position, no checks for selling')