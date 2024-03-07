# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 10:56:51 2024

@author: WCMcGowen
"""

#stocks I am looking at
stock_list = ['AAPL', 'TSLA', 'FAAR', 'AGEN', 'CHCI']

from statistics import mean
import robin_stocks.robinhood as robin


#defines if the market is open
def Is_Open():
    market = robin.get_market_today_hours('XNAS')
    market_available = market['is_open']
    return(market_available)


#gets the current price of a stock
def Quote(ticker):
    price = robin.get_latest_price(ticker)
    price = float(price.pop())
    return price

def ShouldBuy():
    prices_table = Historicals()
    BuyList = []
    BuyDict = {}
    for row in Historicals():
        price_range = row[2] - row[1]
        current = row[-1]
        price_min = row[1]
        tester = price_min + (price_range / 3) # figure out what percent of range you want price in. Right now it must be within bottom third of range. 
        if current <=  tester:
            BuyList.append(True)
        else:
            BuyList.append(False)
    for i in range(len(stock_list)):
        BuyDict[stock_list[i]] = BuyList[i]
    return(BuyDict)
    
#Gets min and max of stocks from above list from 3 month period taken every day
def Historicals():
    OP = 'open_price'
    CP = 'close_price'
    HP = 'high_price'
    LP = 'low_price'
    results = []
    min_max_avg = []
    for stock in stock_list:
        history = robin.get_stock_historicals(stock, 'day', '3month', 'regular', 'close_price')
        results.append(history)
    for i in range(len(stock_list)):
        row = [stock_list[i]] 
        row.append(float(f'{float(min(results[i])):.2f}'))
        row.append(float(f'{float(max(results[i])):.2f}'))
        row.append(float(f'{float(Quote(stock_list[i])):.2f}'))
        min_max_avg.append(row)
    return(min_max_avg) 

def Main():
    from tabulate import tabulate
    login = robin.login(('Liammcg0905@gmail.com'),('E3awacs123'))
    if Is_Open():
        prices = Historicals()
        headers = ['Tic', 'Min', ' Max', ' Now']
        table = tabulate(prices, headers, tablefmt='grid')
        print(table)
    BuyDictionary = ShouldBuy()
    return(BuyDictionary)
            
                