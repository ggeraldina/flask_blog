""" Updating static files by adding a variable """

import os

from flask import url_for

from . import APP


@APP.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(APP.root_path, endpoint, filename)
            values['version'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
