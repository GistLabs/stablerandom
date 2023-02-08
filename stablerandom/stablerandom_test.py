# Copyright (c) 2023 John Heintz, Gist Labs https://gistlabs.com
# License Apache v2 http://www.apache.org/licenses/

import numpy.random
import pytest
from stablerandom import stablerandom
from stablerandom.stablerandom import _randomLocalStack

def random():
    return numpy.random.triangular(1,5,10)

@stablerandom
def stable():
    return numpy.random.triangular(1, 5, 10)

@stablerandom
def nested():
    return stable(), stable(), random()

def test_random_is_random():
    assert random() != random()

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