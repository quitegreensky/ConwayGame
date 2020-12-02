import functools
import time 

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()
        value = func(*args, **kwargs)
        end_time = time.time()
        func_time = end_time- start_time
        print(f"{func.__name__} finished in {round(func_time,4)}")
        return value
    return wrapper_timer