#!/usr/bin/python
# coding=utf-8

"""Initialize application."""


import os
from os.path import join, dirname

import cloudinary
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

cors = CORS()
marsh = Marshmallow()
db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)

from deblurrer.api import api_bp


def create_app(config='flask_config.Production'):
    """
    Init core application.

    Args:
        config: can be import to object or the object itself

    Returns:
        Application instance
    """
    # Load .env vars
    dotenv_path = join(dirname(dirname(__file__)), '.env')
    load_dotenv(dotenv_path)

    # Setup default production config
    app = Flask('deblurrer', instance_relative_config=True)
    app.config.from_object(config)

    # Sentry config
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DNS'),
        integrations=[FlaskIntegration()]
    )

    # Init Cloudinary credentials
    cloudinary.config(
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key = os.environ.get('CLOUDINARY_API_KEY'),
        api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    )

    # Init Plugins
    cors.init_app(app)
    marsh.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    with app.app_context():
        app.register_blueprint(api_bp, url_prefix='/api')

        # Create tables for models
        db.create_all()

        return app
