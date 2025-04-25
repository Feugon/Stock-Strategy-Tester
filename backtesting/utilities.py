from dataclasses import dataclass    
import numpy as np 
import pandas as pd 


@dataclass
class StrategyResult:
    total_return_percent: float
    num_trades: int
    return_per_trade: float
    sharpe: float
    buy_dates: list = None
    sell_dates: list = None


def calculate_sharpe(daily_percent_profit):
    """ Calculate the sharpe ratio of a given return np.array"""
    return round(np.sqrt(252) * np.mean(daily_percent_profit) / np.std(daily_percent_profit),3)

def calculate_sma(stock_prices, sma_timeframe):
    """ Calculate the SMA usen given prices and for the amount of days specifed"""
    return stock_prices.rolling(window = sma_timeframe).mean()


