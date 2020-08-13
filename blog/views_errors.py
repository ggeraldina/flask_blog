""" This file contains the routings and the view error pages """
from flask import render_template

from . import APP


@APP.errorhandler(404)
def page_not_found(_):
    return render_template('error_pages/page_not_found.html'), 404

@APP.errorhandler(500)
def page_server_error(_):
    return render_template('error_pages/page_server_error.html'), 500
