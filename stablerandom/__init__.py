# Copyright (c) 2023 John Heintz, Gist Labs https://gistlabs.com
# License Apache v2 http://www.apache.org/licenses/
import os
from .stablerandom import *

__version__ = "0.1.18"

path = os.getcwd()
if os.path.exists(f'{path}\\__build_version.py') is True:
    with open('__build_version.py') as f:
        lines = f.read()
    __version__ = f"{__version__}.{lines.strip()}"