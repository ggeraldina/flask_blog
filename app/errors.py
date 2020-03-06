from app import app
from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('blog/page_not_found.html'), 404

@app.errorhandler(500)
def page_server_error(error):
    return render_template('blog/page_server_error.html'), 500
