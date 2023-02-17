# Copyright (c) 2023 John Heintz, Gist Labs https://gistlabs.com
# License Apache v2 http://www.apache.org/licenses/
from .stablerandom import *

__version__ = "0.1"
try:
    from .__build_version import build_version
    __version__ = f'{__version__}.{build_version}'
except ImportError:
    pass
