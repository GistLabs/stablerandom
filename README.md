# stablerandom
stablerandom provides a stable and repeatable implementation of 
the NumPy random number generator (numpy.random). With this package, 
you can generate the same sequence of random numbers across different 
platforms and Python environments, ensuring reproducibility 
in scientific computing, machine learning, and unit testing.

stablerandom can decorate any function or method and provide a 
call-stack scoped seeded random generator. It is thread safe and 
supports nested scopes.

## Example
Using the `@stablerandom` decorator to get a stable output for numpy.random.triangular

 ```
import numpy.random
from stablerandom import stablerandom

@stablerandom
def random_triangular(samples):
    return numpy.random.triangular(1, 5, 10, samples)

print(random_triangular(3))
>>> [1.99882862 7.95097645 7.68974243]
print(random_triangular(3))
>>> [1.99882862 7.95097645 7.68974243]
```

## Installing
```bash
$ pip install stablerandom
```
The source code is currently hosted on GitHub at 
https://github.com/GistLabs/stablerandom
and published in PyPI at https://pypi.org/project/stablerandom/ 

The versioning scheme currently used is {major}.{minor}.{auto build number}
from `git rev-list --count HEAD`. 

We recommend picking a version like:

`stablerandom = "^0.5"`

## Dependencies
This library has been tested with [NumPy](https://www.numpy.org) back to version 1.22

## Community guidelines
We welcome contributions and questions. Please head over to github and 
send us pull requests or create issues!
