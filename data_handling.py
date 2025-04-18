import requests
import os
import json
from flask import Flask
from models import stockData                              
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


def convert_dict_to_objects(data, Ticker):
    """ Returns a list of stockData objects from a JSON dictionary.
        Args:
            data (dict): Dictionary of data
            Ticker (str): Ticker symbol
        Returns:
            list: List of objects

    """
    result= []

    for row in data:
        stock_date = datetime.strptime(row, '%Y-%m-%d')
        result.append(stockData(ticker = Ticker, date = stock_date, 
        low = data[row]['3. low'], 
        high = data[row]['2. high'],
        open = data[row]['1. open'], 
        close = data[row]['4. close'],
        volume = data[row]['5. volume']
        ))
        
    return result





def update_data(Ticker, app, db, overwrite = False):
    """ Updates the database with the latest data from the API.
        Args:
            Ticker (str): Ticker symbol
            overwrite (bool): Whether to overwrite existing data
            app (Flask): Flask app
            db (SQLAlchemy): SQLAlchemy object
        Returns:
            None
    """
    STOCK_API_KEY = os.getenv("STOCK_API_KEY")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={Ticker}&apikey={STOCK_API_KEY}'
    r = requests.get(url)
    data = r.json()
    data = data['Time Series (Daily)']
    
    #TODO: Add some tests to make sure the data is valid

    with app.app_context():
        tickr_found = db.session.query(
        db.session.query(stockData).filter_by(ticker="AAPL").exists()).scalar()

        if tickr_found and not overwrite:
            print("Data already exists")
        else:
            DBobjects = convert_dict_to_objects(data, Ticker)
            db.session.bulk_save_objects(DBobjects)

        db.session.commit()
        print("Data inserted")