# stablerandom
stablerandom provides a stable and repeatable implementation of the NumPy random number generator (numpy.random).
With this package, you can generate the same sequence of random numbers across different platforms and Python environments, ensuring reproducibility in scientific computing, machine learning, and other applications.


Installing
==========
```bash
$ pip install stablerandom
```


## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/GistLabs/stablerandom


## Dependencies
- [NumPy - Adds support for large, multi-dimensional arrays, matrices and high-level mathematical functions to operate 
on these arrays](https://www.numpy.org)


## Example
- Using the `@stablerandom` decorator to get a steady output for numpy.random.triangular

 ```
import numpy.random
from stablerandom import stablerandom

@stablerandom
def random_triangular():
    return numpy.random.triangular(1, 5, 10)


print(random_triangular())
print(random_triangular())
print(random_triangular())
```

_OUTPUT_
```
>>> 1.9988286210209485
>>> 1.9988286210209485
>>> 1.9988286210209485
```


## Community guidelines
While the author can be contacted directly for support, it is recommended that third parties use GitHub standard features, 
such as issues and pull requests, to contribute, report problems, or seek support.
