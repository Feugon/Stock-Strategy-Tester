import pandas as pd
import numpy as np
import backtesting.strategies as strat
import backtesting.utilities as util

STRATEGY_MAP = {
    'buy and hold': strat.buy_and_hold
}

def test_strategy(data, strategy,  **kwargs):
    """Tests a strategy on a given dataset."""
    if strategy not in STRATEGY_MAP:
        raise ValueError(f"Strategy {strategy} not found.")
    
    buy_dates, sell_dates = STRATEGY_MAP[strategy](data, **kwargs)
    #TODO need support for kwargs, e.g. how much money we are starting with
    shares_owned = 0
    holdings_value = 0
    cash_value = 0
    percent_returns = []
    initial_portfolio_value = None

    # This does not work properly I think
    for index, entry in data.iterrows():
        if entry['date'] in buy_dates:
            shares_owned += 1    
            cash_value -= entry['close']
        elif entry['date'] in sell_dates:
            shares_owned -= 1
            cash_value += entry['close'] 
        
        holdings_value = entry['close'] * shares_owned
        portfolio_value = holdings_value + cash_value
        
        if initial_portfolio_value is None and portfolio_value != 0:
            initial_portfolio_value = portfolio_value
            percent_diff = (portfolio_value - initial_portfolio_value) / initial_portfolio_value
            percent_returns.append(percent_diff)
        elif initial_portfolio_value is None or portfolio_value == 0:
            percent_returns.append(0)
        
    sharpe = util.calculate_sharpe(percent_returns)
    num_of_trades = len(buy_dates)
    percent_gained = (holdings_value + cash_value - initial_portfolio_value) / initial_portfolio_value

    return util.StrategyResult(percent_gained,num_of_trades,percent_gained / num_of_trades, sharpe)

