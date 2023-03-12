"""Decorators for protecting the API"""
from functools import wraps

from flask import abort, Response, session


class AuthError(Exception):
    """AuthError Class: handles errors"""
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def requires_auth(f):
    """
    Use on routes that require a valid session, otherwise it aborts with a 403
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user') is None:
            return abort(Response("Unauthorized", 403))

        return f(*args, **kwargs)

    return decorated
