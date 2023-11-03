"""setup.py
"""
from setuptools import setup, find_packages


setup(
    name="music",
    author="Frank Lehner",
    version="0.0.1",
    packeges=find_packages(),
    install_requires=[
        "flask",
        "flask-bootstrap",
        "flask-login",
        "flask-migrate",
        "flask-sqlalchemy",
        "flask-mail",
        "wtforms",
        "werkzeug",
        "pyjwt",
        "mypy",
    ],
    test_requires=[
        "pytest",
    ],
)
