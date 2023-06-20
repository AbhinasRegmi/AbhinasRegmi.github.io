import asyncio
from collections import OrderedDict
from functools import wraps, _make_key


def async_lru_cache(maxsize: int = 128):
    cache = OrderedDict()

    async def run_and_cache(func, *args, **kwargs):
        """
        Run your func and store the result in the cache.
        """
        key = _make_key(args, kwargs, False)
        result = await func(*args, **kwargs)
        cache[key] = result

        if len(cache) > maxsize:
            cache.popitem(False)
        
        return result
    
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            key = _make_key(args, kwargs, False)

            if key in cache:
                if isinstance(cache[key], asyncio.Future):
                    return cache[key]
                else:
                    future = asyncio.Future()
                    future.set_result(cache[key])
                    
                    return future
            else:
                task = asyncio.Task(run_and_cache(func, args, kwargs))
                cache[key] = task

                return task
            
        return decorator
    
    if callable(maxsize):
        return wrapper(maxsize)
    else:
        return wrapper
                