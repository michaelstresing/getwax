from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import ProductionConfig, DevelopmentConfig

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=False)

def create_app():
    """Construct the core application."""
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    
    with app.app_context():

        # Imports
        # from . import routes

        # Create tables for models
        db.create_all()

        return app