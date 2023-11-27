"""
Miscellaneous helper functions

Author: Marc Gallet
Date: 2017-06
"""

import hashlib
import logging
import subprocess

from pathlib import Path
from typing import Union

mylogger = logging.getLogger('zkpytb.utils')


def hashfile(filepath: Union[str, Path], hash_method: str = 'sha256', BLOCKSIZE: int = 65536) -> str:
    """Hash a file"""

    hasher = hashlib.new(hash_method)

    with open(str(filepath), 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()


def hashstring(inputstring: bytes, hash_method: str = 'sha256') -> str:
    """Hash a string"""

    hasher = hashlib.new(hash_method)
    hasher.update(inputstring)
    return hasher.hexdigest()


def get_git_hash(rev: str = 'HEAD') -> str:
    """Get the git hash of the current directory"""

    git_hash = ''
    try:
        git_out = subprocess.check_output(['git', 'rev-parse', rev], universal_newlines=True)
    except subprocess.CalledProcessError:
        mylogger.exception("Couldn't determine the git hash!")
    else:
        git_hash = git_out.strip()

    return git_hash
