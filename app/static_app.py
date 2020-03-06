from app import app
import os
from flask import send_from_directory

@app.route('/app/static/css/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join('.', 'app', 'static', 'css'), filename)