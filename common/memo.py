# memo.py - Memoize decorators.
__version__ = '0.1'
__all__ = ['memo', 'memoiter']


Tee = tee([], 1)[0].__class__


def memo(function):
    from functools import wraps as wrap

    memo = {}

    @wrap(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv

    return wrapper


# Memoize Generators
def memoiter(func):
    from itertools import tee
    from types import GeneratorType

    cache={}

    def ret(*args):
        if args not in cache:
            cache[args]=func(*args)
        if isinstance(cache[args], (GeneratorType, Tee)):
            # the original can't be used any more,
            # so we need to change the cache as well
            cache[args], r = tee(cache[args])
            return r
        return cache[args]
    return ret
