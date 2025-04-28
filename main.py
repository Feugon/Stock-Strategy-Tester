from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from configs import ProductionConfig, DevelopmentConfig
from data.update import update_data
from data.fetch import fetch_data
import pandas as pd
from models import db
from backtesting.strategyTester import test_strategy


""" This is an idea, but we can define some global bool for if there was a strategy run, if so then in chart-data we add
buy and sell dates as well, and modify the chart.js shit.
After any route we set the bool back to false or maybe just after /chart-data we set it back to false."""

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
        ticker = request.args.get('ticker', 'AAPL')
        strategy_info = session.pop('strategy_info', None)
        return render_template('chart.html', ticker=ticker, strategy_info=strategy_info)
   
        
        
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
            if session.get('stratHasRun', False):
                session['stratHasRun'] = False

                return jsonify({
                    'prices' : data,
                    'buy_dates' : session['strategyBuy'],
                    'sell_dates' : session['strategySell']
                }) 
            return jsonify({'prices' : data})

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
            elif strategy == 'MeanReversion':
                window = int(request.form.get('window', 20))
                threshold = float(request.form.get('threshold', 2)) / 100  # Convert from percentage
                kwargs = {
                    'window': window,
                    'threshold': threshold
                }
            
            try:
                df = fetch_data(app, ticker)
                if df is None:
                    update_data(ticker, app, db)
                    df = fetch_data(app, ticker)

                strategy = test_strategy(df, strategy, **kwargs)
                session['stratHasRun'] = True
                session['strategyBuy'] = [str(d) for d in strategy.buy_dates]
                session['strategySell'] = [str(d) for d in strategy.sell_dates]
                # Format strategy summary as a user-friendly string
                if hasattr(strategy, 'total_return_percent') and hasattr(strategy, 'num_trades') and hasattr(strategy, 'return_per_trade') and hasattr(strategy, 'sharpe'):
                    summary = f"Total return: {getattr(strategy, 'total_return_percent', 0):.2f}%. Number of trades: {getattr(strategy, 'num_trades', 0)}. Return per trade: {getattr(strategy, 'return_per_trade', 0):.2f}%. Sharpe ratio: {getattr(strategy, 'sharpe', 0):.2f}."
                else:
                    summary = str(strategy)
                session['strategy_info'] = {
                    'total_return_percent': getattr(strategy, 'total_return_percent', 0),
                    'num_trades': getattr(strategy, 'num_trades', 0),
                    'return_per_trade': getattr(strategy, 'return_per_trade', 0),
                    'sharpe': getattr(strategy, 'sharpe', 0),
                    'buy_dates': session['strategyBuy'],
                    'sell_dates': session['strategySell']
                }
                # Redirect to chart page with the ticker to visualize the strategy results
                return redirect(url_for('hello_world', ticker=ticker))
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


    app.run(debug = True)
