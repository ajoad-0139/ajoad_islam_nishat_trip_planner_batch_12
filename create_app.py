from flask import Flask
from app_logging import setup_logging
from app.routes import setup_blueprints
from setup_sqpalchemy import setup_sqlalchemy
from app.errors import setup_error_handler

def create_app (Config) :
    app = Flask(__name__)
    app.config.from_object(Config)
    app = setup_logging(app)
    app = setup_blueprints(app)
    app = setup_sqlalchemy(app)
    app = setup_error_handler(app)

    return app
