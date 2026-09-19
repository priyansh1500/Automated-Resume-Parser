# app/__init__.py
#
# Initializes the Flask application and SQLAlchemy database instance.

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize global SQLAlchemy instance
db = SQLAlchemy()


def create_app():
    """
    Create and configure the Flask application.
    Returns the configured app object.
    """
    app = Flask(__name__)

    # Load configuration settings from Config class in config.py
    from config import Config
    app.config.from_object(Config)

    # Ensure uploads directory exists on disk
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Bind SQLAlchemy database instance to the Flask app
    db.init_app(app)

    # Register blueprints (routes)
    from app import routes
    app.register_blueprint(routes.bp)

    # Create database tables automatically if they do not exist
    with app.app_context():
        from app import models
        db.create_all()

    return app
