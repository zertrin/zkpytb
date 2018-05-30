#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `dicts` module of `zkpytb` package."""

import pytest
import sys


from zkpytb.dicts import (
    AutoDict,
    AutoOrderedDict,
    filter_dict_callfunc,
    filter_dict_only_scalar_values,
    filter_dict_with_keylist,
    mergedicts,
    dict_stable_json_repr,
    hashdict,
)


def dummyfunc():
    return


@pytest.fixture(scope='module',
                params=[None, 0, 1, 3.14, set(), 'string', True, dict(), list()],
                ids=['none', '0', '1', 'float', 'set', 'string', 'bool', 'dict', 'list'])
def not_a_callable(request):
    return request.param


@pytest.fixture(scope='module',
                params=[None, 0, 1, 3.14, set(), 'string', True, list(), dummyfunc],
                ids=['none', '0', '1', 'float', 'set', 'string', 'bool', 'list', 'func'])
def not_a_dict(request):
    return request.param


@pytest.fixture(scope='module',
                params=[None, 0, 1, 3.14, set(), 'string', True, dict(), dummyfunc],
                ids=['none', '0', '1', 'float', 'set', 'string', 'bool', 'dict', 'func'])
def not_a_list(request):
    return request.param


@pytest.fixture(scope='module')
def dict1():
    return {
        'a': 1,
        'b': 2,
        'c': [7, 8],
        'd': (4, 5),
        'e': {'e1': None, 'e2': 'test'},
        'f': dummyfunc,
        'n': None,
    }


@pytest.fixture(scope='module')
def dict2():
    return {
        'e': {'e2': 'test2', 'e3': {'e3a': 0, 'e3b': [None]}},
        'x': 'xxx',
    }


def test_filter_dict_callfunc_not_a_dict(not_a_dict):
    with pytest.raises(AssertionError):
        filter_dict_callfunc(not_a_dict, dummyfunc)


def test_filter_dict_callfunc_not_a_callable(not_a_callable):
    with pytest.raises(AssertionError):
        filter_dict_callfunc({}, not_a_callable)


def test_filter_dict_callfunc(dict1):
    res = filter_dict_callfunc(dict1, lambda k, v: k in 'abfn')
    assert sorted(list(res.keys())) == ['a', 'b', 'f', 'n']
    res = filter_dict_callfunc(dict1, lambda k, v: isinstance(v, (list, dict)))
    assert sorted(list(res.keys())) == ['c', 'e']


def test_filter_dict_only_scalar_values_not_a_dict(not_a_dict):
    with pytest.raises(AssertionError):
        filter_dict_only_scalar_values(not_a_dict)


def test_filter_dict_only_scalar_values(dict1):
    res = filter_dict_only_scalar_values(dict1)
    assert sorted(list(res.keys())) == ['a', 'b', 'f', 'n']


def test_filter_dict_with_keylist_not_a_dict(not_a_dict):
    with pytest.raises(AssertionError):
        filter_dict_with_keylist(not_a_dict, [])


def test_filter_dict_with_keylist_not_a_list(not_a_list):
    with pytest.raises(AssertionError):
        filter_dict_with_keylist({}, not_a_list)


def test_filter_dict_with_keylist(dict1):
    res = filter_dict_with_keylist(dict1, ['a', 'd'])
    assert sorted(list(res.keys())) == ['a', 'd']


def test_filter_dict_with_keylist_blacklist(dict1):
    blacklist = ['a', 'd']
    orig_keys = set(dict1.keys())
    res = filter_dict_with_keylist(dict1, blacklist, blacklistmode=True)
    res_keys = set(res.keys())
    assert res_keys == orig_keys - set(blacklist)


def test_mergedicts_1(dict1, dict2):
    res = dict(mergedicts(dict1, dict2))
    expected_res = {
        'a': 1,
        'b': 2,
        'c': [7, 8],
        'd': (4, 5),
        'e': {'e1': None, 'e2': 'test2', 'e3': {'e3a': 0, 'e3b': [None]}},
        'f': dummyfunc,
        'n': None,
        'x': 'xxx',
    }
    assert res == expected_res


def test_mergedicts_not_a_dict(dict1, not_a_dict):
    with pytest.raises(AssertionError):
        dict(mergedicts(dict1, not_a_dict))


def test_hashdict_not_a_dict(not_a_dict):
    with pytest.raises(AssertionError):
        hashdict(not_a_dict)


def test_hashdict_1(dict2):
    py36 = sys.version_info >= (3, 6)
    res = {}
    res['default'] = hashdict(dict2)
    methods = ['sha1', 'sha256', 'sha512', 'md5']
    if py36:
        methods += ['blake2b', 'blake2s']
    for m in methods:
        res[m] = hashdict(dict2, method=m)
    assert res['sha1'] == '5fa3c59b2295cdb4c7a01c20e086971a0bcfcb7d'
    assert res['sha256'] == 'ca7b51eb5b04a2c8aee95b7e731d971ecce750b0bd24ab8c90156e3b1f22aeaa'
    assert res['sha512'] == ('f7fcc1885ef531ba1c4e0e56b3c38f5cd398cbef1778ee404559d6cd34083c32'
                             '88c63dd9fee4834fbea0bc2b8f04cb66309d4468ba55ad47c76961cd293e20dc')
    assert res['md5'] == 'e1926c486437ca20489d4c35210db768'
    if py36:
        assert res['blake2b'] == ('01303535c6f0b50006d31d36843489d8ec9364a60f85a2802e53676fa78fd671'
                                  '9251664cd7dea5af3f46f7b6625b35e55c71863e99e624d687bbb32440bd573d')
        assert res['blake2s'] == '7b418c386652a926453cefc8fcc0710a13e527c98980df2295c73a11c4bb9374'
    assert res['default'] == res['sha1']


def test_hashdict_2():
    import datetime
    import decimal
    import pathlib
    import uuid
    d = {
        'None': None,
        'bool': True,
        'int': 123456789,
        'complex': 1 + 2j,
        'float': 3.14159,
        'infinity': float('inf'),
        'nan': float('nan'),
        'string': 'lalala',
        'decimal': decimal.Decimal('1.1618'),
        'pathlib.Path': pathlib.Path('test/a/path.test'),
        'datetime.timedelta': datetime.timedelta(days=1, minutes=2, seconds=3),
        'datetime.date': datetime.date(2007, 12, 5),
        'datetime.time': datetime.time(17, 28, 59),
        'datetime.datetime': datetime.datetime(2007, 12, 5, 17, 28, 59),
        'uuid': uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}'),
    }
    d_json_repr = dict_stable_json_repr(d)
    assert d_json_repr == (
        '''{"None": null, "bool": true, "complex": "(1+2j)", "datetime.date": "2007-12-05",'''
        ''' "datetime.datetime": "2007-12-05T17:28:59", "datetime.time": "17:28:59", "datetime.timedelta": 86523.0,'''
        ''' "decimal": "1.1618", "float": 3.14159, "infinity": Infinity, "int": 123456789, "nan": NaN,'''
        ''' "pathlib.Path": "test/a/path.test", "string": "lalala", "uuid": "00010203-0405-0607-0809-0a0b0c0d0e0f"}'''
    )
    res = hashdict(d)
    assert res == '1aa572054769b78af1e9ed7cbd70cc1cb149a90b'


def test_hashdict_3():
    with pytest.raises(TypeError):
        hashdict({'lambda': lambda x: x})


def test_autodict(base_class=AutoDict):
    adict = base_class()
    assert isinstance(adict, dict)
    assert isinstance(adict['x'], base_class)
    assert isinstance(adict['x']['y'], base_class)
    assert isinstance(adict['x']['y']['z'], base_class)
    adict['a'] = 123
    assert adict['a'] == 123
    adict['b']['b1'] = 456
    assert adict['b']['b1'] == 456
    adict['b']['b2'] = 789
    assert adict['b']['b2'] == 789
    adict['c']['c1']['c11'] = 999
    assert adict['c']['c1']['c11'] == 999
    adict['d'] = {}
    with pytest.raises(KeyError):
        adict['d']['d1']['d2'] = None
    adict_as_dict = adict.to_dict()
    assert not isinstance(adict_as_dict, base_class)
    assert not isinstance(adict_as_dict['b'], base_class)
    with pytest.raises(KeyError):
        adict_as_dict['e']['e1']['e2'] = None
    if isinstance(adict, AutoOrderedDict):
        assert list(adict.keys()) == ['x', 'a', 'b', 'c', 'd']


def test_autoordereddict():
    test_autodict(base_class=AutoOrderedDict)
