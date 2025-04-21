from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs import ProductionConfig, DevelopmentConfig
from data.update import update_data
from data.fetch import fetch_data
import pandas as pd
from models import db
from backtesting.strategyTester import test_strategy



def create_app(config = None):
    """Creates a Flask app.
    Args:
        config: Config object
    Returns:
        app: Flask app
    """
    app = Flask(__name__)

    if config:
        app.config.from_object(config)    
    else:
        app.config.from_object(DevelopmentConfig)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app



if __name__ == "__main__":
    app = create_app()

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    df = fetch_data(app,'AAPL')
    obj = test_strategy(df,'buy and hold')
    print(obj)

    #app.run(debug = True)