from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy
from app.errors import OperationalException

sqlalchemy_db = SQLAlchemy()


class SqlalchemyAdapter:
    def __init__(self, app):
        if app.config.get("SQLALCHEMY_DATABASE_URI") is not None:
            sqlalchemy_db.init_app(app)
        elif not app.config.get("TESTING"):
            raise OperationalException(
                "SQLALCHEMY_DATABASE_URI not set in config or environment variable, please make sure"
            )


def create_missing_tables(app):
    with app.app_context():                     
        from app import models 

        tables_before = set(inspect(sqlalchemy_db.engine).get_table_names())
        sqlalchemy_db.create_all()             
        tables_after = set(inspect(sqlalchemy_db.engine).get_table_names())

        created = tables_after - tables_before
        if created:
            app.logger.info("Created tables: %s", ", ".join(sorted(created)))
        else:
            app.logger.info("All tables already exist, nothing to create.")


def setup_sqlalchemy(app):
    SqlalchemyAdapter(app)
    create_missing_tables(app)
    return app