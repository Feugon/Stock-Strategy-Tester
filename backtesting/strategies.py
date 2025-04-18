import numpy as np
import pandas as pd
from backtesting.strategyTester import StrategyResult

def calculate_sharpe(returns):
    """ Calculate the sharpe ratio of a given return np.array"""
    return round(np.sqrt(252) * np.mean(returns) / np.std(returns),3)


def buy_and_hold(data):
    """ Buy and hold strategy"""
    prices = data['close']
    daily_profits = prices - prices.iloc[0]
    end_profit = (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0] * 100
    end_profit = round(end_profit,3)
    win_rate = 100 if end_profit > 0 else 0 
    returns = prices.pct_change()

    return StrategyResult(end_profit,win_rate,1,end_profit,calculate_sharpe(returns))