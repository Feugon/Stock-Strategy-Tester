import numpy as np
import pandas as pd
import backtesting.utilities as util


def buy_and_hold(data):
    """Return purhcase and sale dates for a buy and hold strategy"""
    return {data["date"].iloc[0]: 1}, {data["date"].iloc[-1]: 1}


def simple_moving_average(data, short_sma_interval=10, long_sma_interval=30):
    """Return purchase and sale info for a SMA strategy"""
    purchase_info, sell_info = {}, {}
    short_sma_list = np.full(short_sma_interval, None, dtype=float)
    long_sma_list = np.full(long_sma_interval, None, dtype=float)
    short_above_long = False  # This shouldn't simply default to False, look into this

    for index, entry in data[::-1].iterrows():
        short_sma_list[index % short_sma_interval] = entry["close"]
        long_sma_list[index % long_sma_interval] = entry["close"]

        if None in long_sma_list:
            continue

        short_sma_value = np.mean(short_sma_list)
        long_sma_value = np.mean(long_sma_list)

        if not short_above_long and short_sma_value > long_sma_value:
            short_above_long = True
            purchase_info[entry["date"]] = 1
        elif short_above_long and short_sma_value < long_sma_value:
            short_above_long = False
            sell_info[entry["date"]] = 1

    return purchase_info, sell_info


def momentum_swing(data, window=20, jump_threshold=0.05):
    """Return purchase and sale info for a momentum based strategy"""
    purchase_info, sell_info = {}, {}
    holding_shares = False
    reversed_data = data.iloc[::-1].reset_index(drop=True)

    for index, entry in reversed_data.iterrows():
        if index < window:
            continue

        percent_diff = (
            entry["close"] - reversed_data["close"].iloc[index - window]
        ) / reversed_data["close"].iloc[index - window]

        if percent_diff >= jump_threshold and not holding_shares:
            purchase_info[entry["date"]] = 1
            holding_shares = True
        elif percent_diff < jump_threshold and holding_shares:
            sell_info[entry["date"]] = 1
            holding_shares = False

    return purchase_info, sell_info


def mean_reversion(data, window=20, threshold=0.05):
    """Return purchase and sale info for a mean reversion strategy"""
    purchase_info, sell_info = {}, {}
    rolling_mean = data['close'].rolling(window=window).mean()
    holding_shares = False

    for index, entry in data.iterrows():
        if index < window:
            continue

        deviation = (entry['close'] - rolling_mean.iloc[index]) / rolling_mean.iloc[index]

        if deviation <= -threshold and not holding_shares:
            purchase_info[entry['date']] = 1
            holding_shares = True
        elif deviation >= threshold and holding_shares:
            sell_info[entry['date']] = 1
            holding_shares = False

    return purchase_info, sell_info


def rsi_strategy(data, window=14, overbought=70, oversold=30):
    """Return purchase and sale info for an RSI-based strategy"""
    purchase_info, sell_info = {}, {}
    holding_shares = False
    close = data['close']
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    for index, entry in data.iterrows():
        if index < window:
            continue
        rsi_value = rsi.iloc[index]
        if rsi_value <= oversold and not holding_shares:
            purchase_info[entry['date']] = 1
            holding_shares = True
        elif rsi_value >= overbought and holding_shares:
            sell_info[entry['date']] = 1
            holding_shares = False
    return purchase_info, sell_info
