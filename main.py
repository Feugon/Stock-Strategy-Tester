from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configs import ProductionConfig, DevelopmentConfig
from data_handling import update_data
from models import db



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

    app.run(debug = True)