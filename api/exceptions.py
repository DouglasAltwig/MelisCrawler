"""
Custom exceptions module
"""
class BaseError(Exception):
    """Base error exception"""


class InvalidSite(BaseError):
    """Invalid site error exception"""


class TokenExpired(BaseError):
    """Token expired exception"""
