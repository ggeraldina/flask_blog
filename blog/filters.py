""" Filters for templates """
from datetime import datetime

from . import app


@app.template_filter("datetime_format")
def datetime_format(value, dateformat="%d.%m.%Y %H:%M"):
    date = datetime.fromisoformat(value)
    return datetime.strftime(date, dateformat)