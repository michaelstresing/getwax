from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import ProductionConfig, DevelopmentConfig
from oauthlib.oauth2 import WebApplicationClient

# db = SQLAlchemy()
oath_client = None
app = Flask(__name__, instance_relative_config=False)

def create_app():
    global oath_client

    # Construct the core application.
    app.config.from_object(DevelopmentConfig)
    # db.init_app(app)

    oath_client = WebApplicationClient(app.config['CLIENT_ID'])
    
    with app.app_context():

        # Imports
        from . import routes

        # Create tables for models
        # db.create_all()

        return app