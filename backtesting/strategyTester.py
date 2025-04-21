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
    
    purchase_info, sell_info = STRATEGY_MAP[strategy](data, **kwargs)
    #TODO need support for kwargs, e.g. how much money we are starting with
    shares_owned = 0
    holdings_value = 0
    cash_value = 100
    percent_returns = []
    previous_portfolio_value = 100

    for index, entry in data.iterrows():
        if entry['date'] in purchase_info.keys():
            new_shares_amount = (cash_value * purchase_info[entry['date']]) / entry['close']
            shares_owned += new_shares_amount
            cash_value -= entry['close'] * new_shares_amount
        elif entry['date'] in sell_info.keys():
            new_shares_amount = (cash_value * sell_info[entry['date']]) / entry['close']
            shares_owned -= new_shares_amount
            cash_value += entry['close'] * new_shares_amount
        
        holdings_value = entry['close'] * shares_owned
        portfolio_value_today = holdings_value + cash_value
        percent_returns.append((portfolio_value_today - previous_portfolio_value) / previous_portfolio_value)
        previous_portfolio_value = portfolio_value_today

    sharpe = util.calculate_sharpe(percent_returns)

    num_of_trades = len(purchase_info)
    percent_gained = (portfolio_value_today - 100)

    return util.StrategyResult(percent_gained,num_of_trades,percent_gained / num_of_trades, sharpe)

