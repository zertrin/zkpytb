"""
Miscellaneous helper functions

Author: Marc Gallet
Date: 2017-06
"""

import hashlib


def hashfile(filepath, hash_method='sha256', BLOCKSIZE=65536):
    """Hash a file"""

    hasher = hashlib.new(hash_method)

    with open(str(filepath), 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)

    return hasher.hexdigest()
