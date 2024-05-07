"""Module for decorators."""

from models import ContactError, PhoneFormatError

def input_error(strerror: str = "Invalid input."):
    """Decorator for handling input errors.

    Args:
        strerror (str, optional): Message returned in case of invalid input. Defaults to "Invalid input.".
        Can be overridden by passing a custom message to the decorator.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except(ValueError, IndexError, ContactError, PhoneFormatError) as e:
                if hasattr(e, "message"):
                    return f"{strerror}\Error: {e.message}"
                return strerror
        return wrapper
    return decorator
