
__all__ = ["ignore_this", "numpypi_series"]

import os
import subprocess
from os import path
from subprocess import PIPE

# For __version__ add + to check if we are installing from a github repo
__version__ = '1.0.0+'
__released__ = '1.0.0'  # used when Sphinx builds its own docs

#: Version info for better programmatic use.
#:
#: A tuple of five elements; for Sphinx version 1.2.1 beta 3 this would be
#: ``(1, 2, 1, 'beta', 3)``. The fourth element can be one of: ``alpha``,
#: ``beta``, ``rc``, ``final``. ``final`` always has 0 as the last element.
#:
#: .. versionadded:: 1.2
#:    Before version 1.2, check the string ``sphinx.__version__``.
version_info = (1, 0, 0, 'alpha', 0)

package_dir = path.abspath(path.dirname(__file__))

__display_version__ = __version__  # used for command line version
if __version__.endswith('+'):
    # try to find out the commit hash if checked out from git, and append
    # it to __version__ (since we use this value from setup.py, it gets
    # automatically propagated to an installed copy as well)
    __version__ = __version__[:-1]  # remove '+' for PEP-440 version spec.
    __display_version__ = __version__
    try:
        ret = subprocess.run(['git', 'show', '-s', '--pretty=format:%h'],
                             cwd=package_dir,
                             stdout=PIPE, stderr=PIPE)
        if ret.stdout:
            __version__ += '+' + ret.stdout.decode('ascii').strip()
            __display_version__ += '/' + ret.stdout.decode('ascii').strip()
    except Exception:
        pass

