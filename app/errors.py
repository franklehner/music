"""Error handler
"""
from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):  # pylint: disable=unused-argument
    """error handler for not found
    """
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):  # pylint: disable=unused-argument
    """error handler for internal error
    """
    db.session.rollback()
    return render_template("500.html"), 500
