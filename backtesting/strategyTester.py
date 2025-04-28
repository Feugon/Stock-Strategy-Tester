import pandas as pd
import numpy as np
import backtesting.strategies as strat
import backtesting.utilities as util

STRATEGY_MAP = {
    'buy and hold'  :   strat.buy_and_hold,
    'SMA'           :   strat.simple_moving_average,
    'Momentum'      :   strat.momentum_swing,
    'mean reversion':   strat.mean_reversion,
    'RSI'           :   strat.rsi_strategy
}

def run_strategy(strategy_name, stock_df, **kwargs):
    if strategy_name not in STRATEGY_MAP:
        raise ValueError(f"Strategy {strategy_name} not found.")

    purchase_info, sell_info = STRATEGY_MAP[strategy_name](stock_df, **kwargs)
    return purchase_info, sell_info


def test_strategy(stock_df, strategy_name,  **kwargs):
    """Tests a strategy on a given dataset."""
    #TODO need support for kwargs, e.g. how much money we are starting with
    purchase_info, sell_info = run_strategy(strategy_name, stock_df, **kwargs)
    shares_owned = 0
    holdings_value = 0
    cash_value = 100
    percent_returns = []
    previous_portfolio_value = 100

    for index, entry in stock_df[::-1].iterrows():
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

    sharpe = round(util.calculate_sharpe(percent_returns),3)

    num_of_trades = len(purchase_info)
    percent_gained = round((portfolio_value_today - 100),3)

    return util.StrategyResult(percent_gained,num_of_trades, round(percent_gained / num_of_trades,3), sharpe, purchase_info, sell_info)

