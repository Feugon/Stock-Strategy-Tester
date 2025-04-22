from flask import Flask, render_template, request, jsonify
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
    
    @app.route("/chart")
    def chart():
        return render_template('chart.html')
        
    @app.route("/chart-data")
    def chart_data():
        ticker = request.args.get('ticker', 'AAPL')
        try:
            df = fetch_data(app, ticker)
            if df is None:
                update_data(ticker, app, db)
                df = fetch_data(app, ticker)
     
            if df is None:
                return jsonify({'error': 'Failed to fetch data'}), 404

            df['date'] = df['date'].astype(str)
            data = df.to_dict('records')
            
            return jsonify(data)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route("/run-strategy", methods = ['GET', 'POST'])
    def run_strategy():
        if request.method == 'POST':
            print("Hello, Post Request Worked")
            # Get form data
            ticker = request.form.get('ticker')
            strategy = request.form.get('strategy')
            
            # Get strategy-specific parameters
            kwargs = {}
            if strategy == 'SMA':
                short_sma_interval = int(request.form.get('short_sma_interval', 10))
                long_sma_interval = int(request.form.get('long_sma_interval', 30))
                kwargs = {
                    'short_sma_interval': short_sma_interval,
                    'long_sma_interval': long_sma_interval
                }
            elif strategy == 'Momentum':
                window = int(request.form.get('window', 20))
                jump_threshold = float(request.form.get('jump_threshold', 5)) / 100  # Convert from percentage
                kwargs = {
                    'window': window,
                    'jump_threshold': jump_threshold
                }
            
            # Fetch data and run strategy
            try:
                df = fetch_data(app, ticker)
                if df is None:
                    update_data(ticker, app, db)
                    df = fetch_data(app, ticker)

                result = test_strategy(df, strategy, **kwargs)
                return f"<h1>Strategy Results</h1><pre>{result}</pre><p><a href='/run-strategy'>Run Another Strategy</a></p>"
            except Exception as e:
                return f"<h1>Error</h1><p>{str(e)}</p><p><a href='/run-strategy'>Try Again</a></p>"
        
        # GET request - render the form template
        return render_template('run_strategy.html')

    return app



if __name__ == "__main__":
    app = create_app()

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    df = fetch_data(app,'AAPL')
    obj = test_strategy(df, 'SMA')
    print(obj)

    app.run(debug = True)
