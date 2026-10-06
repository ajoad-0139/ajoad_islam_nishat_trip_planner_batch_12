from flask_sqlalchemy import SQLAlchemy
from app.errors import OperationalException

sqlalchemy_db = SQLAlchemy()

class SqlalchemyAdapter  : 
    def __init__(self, app) :
        if app.config['SQLALCHEMY_DATABASE_URI'] is not None :
            sqlalchemy_db.init_app(app)
        elif not app.config['TESTING'] :
            raise OperationalException("SQLALCHEMY_DATABASE_URI not set in config or evnironment variable, please make sure")

def setup_sqlalchemy (app) :
    try :
        SqlalchemyAdapter(app)
    except OperationalException as e:
        raise e
    
    return app
