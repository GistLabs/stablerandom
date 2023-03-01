# Copyright (c) 2023 John Heintz, Gist Labs https://gistlabs.com
# License Apache v2 http://www.apache.org/licenses/
import numpy.random
from numpy.random import Generator, PCG64
import threading


class RandomLocal(threading.local):
    """
    A threadlocal to hold a stack of stable random generators
    """
    stack = []

    def push(self):
        """Push a new Generator PCG64 SeedSequence to the stack"""
        self.stack.append(Generator(PCG64(123456789)))

    def pop(self):
        """Removes the top element from the stack"""
        self.stack.pop(0)

    def top(self) -> numpy.random.Generator:
        """Lookup the top random generator, or return None

        Returns
        -------
        numpy.random.Generator or None
            Top random generator, or None on failure.
        """
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return None


_randomLocalStack = RandomLocal()
_globalRandomGenerator = Generator(PCG64())


def random() -> Generator:
    """
    Return a Generator,either the current stable one or else a (random) global Generator

    This can be used for all cases to get random numbers, whether inside a @stablerandom or not

    """
    return _randomLocalStack.top() or _globalRandomGenerator


def stablerandom(func):
    """A decorator indicating stable random
    @stablerandom provides stable random behavior for a function and call stack

    Usage:
        @stable_random
        def my_method():
            ...
    """
    def wrapper(*args, **kwargs):
        _randomLocalStack.push() # push a new stable random Generator on to the stack

        try:
            return func(*args, **kwargs) # call the function and this might make random().function calls
        finally:
            _randomLocalStack.pop() # clear thread local

    return wrapper


# random functions to wrap for stable,
# from https://numpy.org/doc/stable/reference/random/legacy.html#functions-in-numpy-random


# List of all available numpy.random functions
_random_functions = [x for x in dir(numpy.random) if not x.startswith('_')]

# Dictionary Mapping numpy.random functions to their equivalents available on the Generator
_random_dictionary = {'randint': 'integers', 'random_integers': 'integers',
                      'sample': 'random', 'ranf': 'random', 'random_sample': 'random'}


def _wrap_numpy_random(funcName):
    _orig = getattr(numpy.random, funcName)

    def _stable(*args, **kwargs):
        stable = _randomLocalStack.top()
        if stable:
            try:
                # Get the attribute of the function name from the Generator
                func = getattr(stable, funcName)
            except AttributeError:
                # The Generator does not possess requested function name
                try:
                    # Get the function equivalent available on the Generator from `_random_dictionary`
                    func = getattr(stable, _random_dictionary[funcName])
                except (KeyError, AttributeError):
                    # The Generator does not possess an equivalent of the function
                    func = _orig  # Return the original function from numpy.random
            return func(*args, **kwargs)
        else:
            return _orig(*args, **kwargs)

    setattr(numpy.random, funcName, _stable)


[_wrap_numpy_random(f) for f in _random_functions]
