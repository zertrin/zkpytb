#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `zkpytb` package."""

import pytest
from pytest import approx, raises

np = pytest.importorskip("numpy")  # noqa
pd = pytest.importorskip("pandas")  # noqa

from numpy.testing import assert_array_equal

from zkpytb.pandas import (
    compare_df_cols,
    df_query_with_ratio,
    move_col_to_beginning_of_df,
    only_outliers,
    remove_outliers,
    tdescr,
)


def dummyfunc():
    return


@pytest.fixture(scope='module',
                params=[None, 0, 1, 3.14, set(), 'string', True, dict(), list(), dummyfunc],
                ids=['none', '0', '1', 'float', 'set', 'string', 'bool', 'dict', 'list', 'func'])
def not_a_df(request):
    return request.param


def generate_test_df(df_len, rand_seed):
    return pd.DataFrame({
        'a': np.zeros(df_len),
        'b': np.ones(df_len),
        'c': np.arange(df_len) + 1,
        'd': np.arange(df_len, dtype=float),
        'e': np.random.RandomState(rand_seed).rand(df_len),
        'f': np.random.RandomState(rand_seed).randn(df_len),
        'g': np.random.RandomState(rand_seed).random_integers(0, 100, df_len),
        'n': np.zeros(df_len) + np.nan,
    }, index=range(df_len))


@pytest.fixture(scope='module')
def df1():
    return generate_test_df(df_len=10, rand_seed=123456)


@pytest.fixture(scope='module')
def df2():
    return generate_test_df(df_len=10, rand_seed=998877)


def test_tdescr_not_a_df(not_a_df):
    with raises(AttributeError, match="has no attribute 'describe'"):
        tdescr(not_a_df)


def test_df_query_with_ratio_not_a_df(not_a_df):
    with raises(AttributeError, match="has no attribute 'query'"):
        df_query_with_ratio(not_a_df, '')


def test_df_query_with_ratio(df1):
    res, ratio = df_query_with_ratio(df1, 'c > 5')
    assert ratio == approx(0.5)
    assert_array_equal(res.index, np.arange(5, 10))


def test_remove_outliers(df1):
    res = remove_outliers(df1, 'f', 1)
    assert_array_equal(res.index, [1, 2, 3, 5, 6, 7, 8])


def test_only_outliers(df1):
    res = only_outliers(df1, 'f', 1)
    assert_array_equal(res.index, [0, 4, 9])


def test_move_col_to_beginning_of_df(df1):
    res = move_col_to_beginning_of_df(df1, 'e')
    assert_array_equal(res.columns, ['e', 'a', 'b', 'c', 'd', 'f', 'g', 'n'])


@pytest.mark.xfail(reason="To investigate...")
def test_compare_df_cols(df1, df2):
    res1 = compare_df_cols([df1, df2], ['e', 'f', 'g'], mode=1)
    assert res1.columns == ['e_1', 'e_2', 'f_1', 'f_2', 'g_1', 'g_2']

    res2 = compare_df_cols([df1, df2], ['e', 'f', 'g'], mode=2)
    assert res2.columns == ['e_1', 'f_1', 'g_1', 'e_2', 'f_2', 'g_2']
