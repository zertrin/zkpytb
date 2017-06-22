"""
Helper functions related to dictionaries

Author: Marc Gallet
Date: 2017-04
"""

# Useful helper functions to filter dictionaries based on key/value characteristics


def filter_dict_callfunc(dict_in, func):
    assert(isinstance(dict_in, dict))
    assert(callable(func))
    return {k: v for (k, v) in dict_in.items() if func(k, v)}


def filter_dict_only_scalar_values(dict_in):
    assert(isinstance(dict_in, dict))
    return {k: v for (k, v) in dict_in.items() if not hasattr(v, '__iter__')}


def filter_dict_with_keylist(dict_in, keylist, blacklistmode=False):
    assert(isinstance(dict_in, dict))
    assert(isinstance(keylist, list))
    if blacklistmode:
        return {k: v for (k, v) in dict_in.items() if k not in keylist}
    else:
        return {k: v for (k, v) in dict_in.items() if k in keylist}


def mergedicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(mergedicts(dict1[k], dict2[k])))
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])
