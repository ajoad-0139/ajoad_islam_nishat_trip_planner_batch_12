from .health import blueprint as health_blueprint

def setup_blueprints(app) :
    app.register_blueprint(health_blueprint, url_prefix="")
    return app

__all__ = ['setup_blueprints']