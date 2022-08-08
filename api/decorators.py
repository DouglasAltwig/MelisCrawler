"""Decorators"""
import time
from functools import wraps

def valid_token(func):
    """Valid token decorator"""
    @wraps(func)
    def helper(*args, **kwargs):
        client = args[0]
        if client.expires_at and not client.expires_at > time.time():
            token = client.refresh_token()
            client.set_token(token)
        return func(*args, **kwargs)

    return helper
