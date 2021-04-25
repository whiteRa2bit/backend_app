from flask import request
from functools import wraps
from werkzeug.exceptions import BadRequest
from marshmallow import ValidationError


def request_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            try:
                schema.load(request.json)
            except ValidationError as err:
                return BadRequest(err.messages)
            return f(*args, **kw)
        return wrapper
    return decorator


def response_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            response, status_code = f(*args, **kw)
            schema.load(response.json)
            return response, status_code

        return wrapper
    return decorator
