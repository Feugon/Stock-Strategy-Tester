import numpy as np
import pandas as pd 
import backtesting.utilities as util 

def buy_and_hold(data):
    """ Return purhcase and sale dates for a buy and hold strategy"""
    return [data['date'].iloc[0]],[data['date'].iloc[-1]] 


# note to self: I'm changing it so the strategy summary gets printed in strategy tester
# now the strategy functions return when we buy and sell, this should make it more combinable later on }
