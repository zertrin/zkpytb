#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `zkpytb` package."""

import pytest


from zkpytb.dicts import (
    filter_dict_callfunc,
    filter_dict_only_scalar_values,
    filter_dict_with_keylist,
    mergedicts,
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


def test_mergedict_1(dict1, dict2):
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
