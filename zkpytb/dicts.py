"""
Helper functions related to dictionaries

Author: Marc Gallet
"""


import hashlib
import json

from collections import OrderedDict

from zkpytb.json import JSONEncoder


class AutoDict(dict):
    """
    Default dict of dicts with infinite nesting (a.k.a. autovivification).
    """
    _base_class = dict

    def __getitem__(self, key):
        try:
            return self._base_class.__getitem__(self, key)
        except KeyError:
            value = self[key] = type(self)()
            return value

    def to_dict(self):
        """
        Convert this AutoDict to a normal dict (without autovivification).
        """
        return self._base_class(
            (key, (val.to_dict() if isinstance(val, AutoDict) else val))
            for key, val in self.items()
        )


class AutoOrderedDict(OrderedDict, AutoDict):
    """
    Default dict of OrderedDicts with infinite nesting (a.k.a. autovivification).
    """
    _base_class = OrderedDict


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
    assert(isinstance(dict1, dict))
    assert(isinstance(dict2, dict))
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


def dict_stable_json_repr(dict_in):
    return json.dumps(dict_in, sort_keys=True, cls=JSONEncoder)


def hashdict(dict_in, method='sha1'):
    assert(isinstance(dict_in, dict))
    h = hashlib.new(method)
    dict_repr = dict_stable_json_repr(dict_in)
    h.update(dict_repr.encode('utf-8'))
    return h.hexdigest()
