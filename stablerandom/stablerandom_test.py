# Copyright (c) 2023 John Heintz, Gist Labs https://gistlabs.com
# License Apache v2 http://www.apache.org/licenses/

import numpy.random
import pytest
from stablerandom import stablerandom, random
from stablerandom.stablerandom import _randomLocalStack
from stablerandom.stablerandom import _globalRandomGenerator


def random_triangular():
    return numpy.random.triangular(1, 5, 10)


@stablerandom
def stable():
    return numpy.random.triangular(1, 5, 10)


@stablerandom
def nested():
    return stable(), stable(), random_triangular()


def test_random_is_random():
    assert random_triangular() != random_triangular()


def test_stable_is_stable():
    assert stable() == stable()


def test_stable_normal():
    @stablerandom
    def stable_normal():
        return numpy.random.normal(10, 5)

    assert stable_normal() == stable_normal()


def test_stable_pareto():
    @stablerandom
    def stable_pareto():
        return numpy.random.pareto(10)

    assert stable_pareto() == stable_pareto()


def test_stable_uniform():
    @stablerandom
    def stable_uniform():
        return numpy.random.uniform(0, 1)

    assert stable_uniform() == stable_uniform()


def test_global():
    assert random() == _globalRandomGenerator

    @stablerandom
    def stableIsNotGlobal():
        assert _globalRandomGenerator != random()
        assert random() == _randomLocalStack.top()
    stableIsNotGlobal()


def test_stable_randint():
    @stablerandom
    def stable_randint():
        return numpy.random.randint(8, size=1)

    assert stable_randint() == stable_randint()


def test_stable_ranf():
    @stablerandom
    def stable_ranf():
        return numpy.random.ranf(1)

    assert stable_ranf() == stable_ranf()


def test_random_dictionary():
    @stablerandom
    def stable_random_sample():
        return numpy.random.random_sample(1)

    @stablerandom
    def stable_sample():
        return numpy.random.sample(1)

    @stablerandom
    def stable_random_integers():
        return numpy.random.random_integers(1)

    assert stable_random_sample() == stable_random_sample()
    assert stable_sample() == stable_sample()
    assert stable_random_integers() == stable_random_integers()


def test_not_wrapped():
    @stablerandom
    def not_wrapped_randn():
        return numpy.random.randn(1)

    @stablerandom
    def not_wrapped_rand():
        return numpy.random.rand(1)

    assert not_wrapped_randn() != not_wrapped_randn()
    assert not_wrapped_rand() != not_wrapped_rand()
