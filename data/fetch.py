from models import stockData
import pandas as pd
from flask import Flask


def fetch_data(app, ticker):
    """Fetches data from the database.
    Args:
        app (Flask): Flask app
        ticker (str): Ticker symbol
    Returns:
        df (pd.DataFrame): Dataframe containing the data
    """
    with app.app_context():
        result = stockData.query.filter_by(ticker=ticker).all()
        df = pd.DataFrame([r.__dict__ for r in result])
        df = df.drop(columns=['_sa_instance_state', 'id','ticker'])

    return df