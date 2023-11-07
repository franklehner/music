"""Configuration
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Class with configuration for Flask app
    """
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
