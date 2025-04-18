from re import S
import pandas as pd
from strategyTester import StrategyResult

def calculate_sharpe(data):
    """ Calculate the sharpe ratio of a given dataframe"""



def buy_and_hold(data):
    """ Buy and hold strategy"""
    buy_price = data.iloc[-1]['close']
    sell_price = data.iloc[0]['close']
    profits = sell_price - buy_price
    win_rate = 100 if profits > 0 else 0 

    return StrategyResult(profits,win_rate,1,profits,)