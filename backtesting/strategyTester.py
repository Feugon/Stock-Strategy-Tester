import pandas as pd
from dataclasses import dataclass

@dataclass
class StrategyResult:
    total_return: float
    win_rate: float
    num_trades: int
    return_per_trade: float
    sharpe: float

# Should return PnL, Win Rate, Number of Trades, Return per trade, Sharpre Ratio 
# Probably should be a dict or maybe a class object
def testStrategy(data,strategy):
    pass