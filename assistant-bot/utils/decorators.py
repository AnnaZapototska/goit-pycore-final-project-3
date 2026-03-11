# decorator for major errors
from unittest import result
from storage import save_data

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            return str(e)
        except Exception as e:
            return "An unexpected error occurred. Please try again."
        finally:
            book = args[1]
            save_data(book)
    return inner

# decorator with user friendly informations
def require_args(count, usage):
    def decorator(func):
        def wrapper(args, book):
            if len(args) < count:
                return f"Usage: {usage}"
            return func(args, book)
        return wrapper
    return decorator