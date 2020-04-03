""" Filters for templates """
from datetime import datetime

from . import APP


@APP.template_filter("datetime_str_format")
def datetime_str_format(value, dateformat="%d.%m.%Y %H:%M"):
    date = datetime.fromisoformat(value)
    return datetime.strftime(date, dateformat)

@APP.template_filter("datetime_format")
def datetime_format(value, dateformat="%d.%m.%Y %H:%M"):
    return datetime.strftime(value, dateformat)
