from .health import blueprint as health_blueprint
from .trips import blueprint as trip_blueprint

def setup_blueprints(app) :
    app.register_blueprint(health_blueprint, url_prefix="")
    app.register_blueprint(trip_blueprint, url_prefix="/api/v1/trips")
    return app

__all__ = ['setup_blueprints']