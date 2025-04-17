from flask import Flask

def create_app(config = None):
    app = Flask(__name__)

    if config:
        app.config.from_object(config)    
    else:
        from configs import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    return app



if __name__ == "__main__":
    app = create_app()
    app.run()