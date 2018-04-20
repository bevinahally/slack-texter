# services/slack_texter/app/__init__.py

import os

from flask import Flask, jsonify


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    from app.api.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    # shell context for flask cli
    return app
