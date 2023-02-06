# Copyright (c) 2023 John Heintz, Gist Labs https://gistlabs.com
# License Apache v2 http://www.apache.org/licenses/
import numpy.random
from numpy.random import Generator, PCG64
import threading


class RandomLocal(threading.local):
    '''A threadlocal to hold a stack of stable randome generators'''
    stack = []

    def push(self):
        '''Push a new Generator PCG64 SeedSequence to the stack'''
        self.stack.append(Generator(PCG64(123456789)))

    def pop(self):
        '''Removes the top element from the stack'''
        self.stack.pop(0)

    def top(self) -> numpy.random.Generator:
        '''Lookup the top random generator, or return None'''
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return None

_randomLocalStack = RandomLocal()

def stablerandom(func):
    """@stablerandom can be used stable random behavior for a function and call stack

    Usage:
        @stable_random
        def my_method():
            ...
    """
    def wrapper(*args, **kwargs):
        _randomLocalStack.push()

        try:
            return func(*args, **kwargs)
        finally:
            # clear thread local
            _randomLocalStack.pop()

    return wrapper

_orig_triangular = numpy.random.triangular
def stable_triangular(*args, **kwargs):
    stable = _randomLocalStack.top()
    if stable:
        return stable.triangular(*args, **kwargs)
    else:
        return _orig_triangular(*args, **kwargs)
setattr(numpy.random, 'triangular', stable_triangular)
#numpy.random.triangular = stable_triangular

_orig_normal = numpy.random.normal
def stable_normal(*args, **kwargs):
    stable = _randomLocalStack.top()
    if stable:
        return stable.normal(*args, **kwargs)
    else:
        return _orig_normal(*args, **kwargs)
numpy.random.normal = stable_normal

def _wrap_numpy_random(funcName):
    _orig = getattr(numpy.random, funcName)

    def _stable(*args, **kwargs):
        stable = _randomLocalStack.top()
        if stable:
            func = getattr(stable, funcName)
            return func(*args, **kwargs)
        else:
            return _orig(*args, **kwargs)

    setattr(numpy.random, funcName, _stable)
_wrap_numpy_random('pareto')