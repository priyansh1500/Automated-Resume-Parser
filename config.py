# config.py
#
# Application configuration settings.
# Automatically loads variables from your private local .env file using python-dotenv.
# Keeps your PostgreSQL credentials safe and out of version control (.gitignore).

import os
from dotenv import load_dotenv

# Load environment variables from local .env file if present
load_dotenv()


class Config:
    # Flask Session & Security Key
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Upload folder configuration
    UPLOAD_FOLDER = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'uploads')
    )
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB upload limit

    # PostgreSQL Database Connection URL
    # Reads from environment variable 'DATABASE_URL' (loaded from .env)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/resume_parser_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
