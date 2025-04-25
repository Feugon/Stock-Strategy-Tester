from models import stockData
import pandas as pd
from flask import Flask



def fetch_data(flask_app_instance, ticker):
    """Fetches data from the database.
    Args:
        flask_app_instance (Flask): Flask app
        ticker (str): Ticker symbol
    Returns:
        df (pd.DataFrame): Dataframe containing the data
    """
    with flask_app_instance.app_context():
        stock_entries = stockData.query.filter_by(ticker=ticker).all()
        if not stock_entries:
            return None

        df = pd.DataFrame([entry.__dict__ for entry in stock_entries])
        df = df.drop(columns=['_sa_instance_state', 'id', 'ticker'])
    return df
