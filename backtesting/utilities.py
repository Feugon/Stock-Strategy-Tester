from dataclasses import dataclass    
import numpy as np 
import pandas as pd 


@dataclass
class StrategyResult:
    total_return_pecent: float
    # win_rate: float
    num_trades: int
    return_per_trade: float
    sharpe: float


def calculate_sharpe(returns):
    """ Calculate the sharpe ratio of a given return np.array"""
    return round(np.sqrt(252) * np.mean(returns) / np.std(returns),3)

def calculate_sma(prices, timeframe):
    """ Calculate the SMA usen given prices and for the amount of days specifed"""
    return prices.rolling(window = timeframe).mean()


