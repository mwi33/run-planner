from flask import Flask

from .adapters.db import init_db, remove_session
from .api import api_bp
from .config import Config
from .web import web_bp


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    try:
        import os

        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    init_db(app)

    app.register_blueprint(web_bp, url_prefix="/")
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.teardown_appcontext
    def cleanup(exception=None):
        remove_session()

    return app
