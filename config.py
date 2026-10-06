import os

class Config(object):
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///trip_planner.db')