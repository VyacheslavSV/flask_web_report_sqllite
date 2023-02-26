import os

from flask import Flask
from src import web_report_app
from config import Config

def create_app(test_config=None, config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.register_blueprint(web_report_app.bp)

    return app


if __name__ == "__main__":
    create_app()
