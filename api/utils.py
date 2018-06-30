from flask import make_response, g
from flask_restful import abort
import sqlite3
from .Errors import errors
from datetime import datetime, timedelta

JSON_MIME_TYPE = 'application/json'

def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(data, status, headers)


def sql_row_to_dict(cursor, row):
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result


def int_to_bool(num):
    if num == 1:
        return True
    else:
        return False


def bool_to_int(bool):
    if bool:
        return 1
    else:
        return -1


def raise_costume_abort(error):
    """abort with a costume massege and code from the errors dict"""
    abort(errors[error]['status'], message=errors[error]['message'])

