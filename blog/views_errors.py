"""This file contains the routings and the view error pages"""
from flask import render_template

from . import app


@app.errorhandler(404)
def page_not_found(error): # pylint: disable=unused-argument
    return render_template('error_pages/page_not_found.html'), 404

@app.errorhandler(500)
def page_server_error(error): # pylint: disable=unused-argument
    return render_template('error_pages/page_server_error.html'), 500
