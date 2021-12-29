'''
NFHS Data Parser - Utilities
Author: Akshay Ranjan <akshay@mlcfoundation.org.in>
MLC Foundation, India
December, 2021
'''

import functools
import time
from os import getpid

# Time code
def time_it(func):
    @functools.wraps(func)
    def timed_func(*args, **kwargs):
        st = time.perf_counter()
        val = func(*args, **kwargs)
        et = time.perf_counter()
        run_time = et - st
        print(f"[{getpid()}] {func.__name__!r} took {run_time:.2f}")
        return val
    return timed_func