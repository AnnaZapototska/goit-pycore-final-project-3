# decorator for major errors
from typing import Any, Callable


def input_error(func: Callable[..., Any]) -> Callable[..., Any]:
    def inner(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, KeyError, IndexError) as e:
            return str(e)
        except BaseException:
            return "An unexpected error occurred. Please try again."

    return inner

# decorator with user friendly informations


def require_args(
    count: int, usage: str
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(args: list[str], book: Any) -> Any:
            if len(args) < count:
                return f"Usage: {usage}"
            return func(args, book)

        return wrapper

    return decorator
