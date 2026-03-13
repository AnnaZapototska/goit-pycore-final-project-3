# decorator for major errors
# def input_error(func):
#     def inner(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except (ValueError, KeyError, IndexError) as e:
#             return str(e)
#         except BaseException:
#             return "An unexpected error occurred. Please try again."
#     return inner

def input_error(func):
    """
    Decorator to catch exceptions and display the exact error message.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Show exact error type and message
            return f"[{type(e).__name__}] {e}"
    return inner


# decorator with user friendly informations
def require_args(count, usage):
    def decorator(func):
        def wrapper(args, book):
            if len(args) != count:
                return f"Usage: {usage}"
            return func(args, book)
        return wrapper
    return decorator
