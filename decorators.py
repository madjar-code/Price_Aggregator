import time
from functools import wraps
from typing import Callable, Any


def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        print(f"Function {func.__name__} for {args[0]}\
                took {duration:.2f} seconds")
        return result
    return wrapper
