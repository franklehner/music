"""setup.py
"""
from setuptools import setup, find_packages


setup(
    name="music",
    author="Frank Lehner",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-bootstrap",
        "flask-login",
        "flask-migrate",
        "flask-sqlalchemy",
        "flask-mail",
        "flask-wtf",
        "wtforms",
        "werkzeug",
        "pyjwt",
        "mypy",
        "pytube",
        "moviepy",
        "bs4",
    ],
    test_requires=[
        "pytest",
    ],
)
