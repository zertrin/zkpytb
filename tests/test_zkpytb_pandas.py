#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the `pandas` module of `zkpytb` package."""

import pytest
from pytest import approx, raises

np = pytest.importorskip("numpy")  # noqa
pd = pytest.importorskip("pandas")  # noqa

from numpy.testing import assert_array_equal

from zkpytb.pandas import (
    extended_percentiles,
    compare_df_cols,
    df_query_with_ratio,
    move_col_to_beginning_of_df,
    only_outliers,
    remove_outliers,
    tdescr,
    mad,
    percentile,
    describe_numeric_1d,
)


describe_numeric_1d_expected_col_list = [
    'count', 'mean', 'std', 'mad', 'mad_c1', 'iqr', 'min', '1%', '5%', '25%', '50%', '75%', '95%', '99%', 'max'
]


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


@pytest.fixture(params=[None, [.1, .25, .5, .75, .9]])
def percentiles(request):
    return request.param


@pytest.fixture(params=[True, False])
def disp(request):
    return request.param


def test_tdescr_df1(df1, percentiles, disp):
    res = tdescr(df1, percentiles=percentiles, disp=disp)
    assert isinstance(res, pd.DataFrame)
    res_rows, res_cols = res.shape
    epl = len(extended_percentiles) if percentiles is None else len(percentiles)
    assert res_cols == 5 + epl
    assert res_rows == len(df1.columns)


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


def test_compare_df_cols_mode1(df1, df2):
    res = compare_df_cols([df1, df2], ['e', 'f', 'g'], mode=1)
    assert list(res.columns) == ['e_1', 'e_2', 'f_1', 'f_2', 'g_1', 'g_2']


def test_compare_df_cols_mode2(df1, df2):
    res = compare_df_cols([df1, df2], ['e', 'f', 'g'], mode=2)
    assert list(res.columns) == ['e_1', 'f_1', 'g_1', 'e_2', 'f_2', 'g_2']


def test_compare_df_cols_mode3(df1, df2):
    res = compare_df_cols([df1, df2], ['e', 'f', 'g'], mode=3)
    assert res is None


def test_mad_df1(df1):
    f = mad()
    assert f.__name__ == 'mad'
    assert f(df1.a) == pytest.approx(0.0)
    assert f(df1.b) == pytest.approx(0.0)
    assert f(df1.c) == pytest.approx(3.7065055462640051)
    assert f(df1.d) == pytest.approx(3.7065055462640051)
    assert f(df1.e) == pytest.approx(0.32667683062127778)
    assert f(df1.f) == pytest.approx(0.93021508625544813)
    assert f(df1.g) == pytest.approx(17.791226622067224)


def test_mad_c1_df1(df1):
    f = mad(c=1, name='mad_c1')
    assert f.__name__ == 'mad_c1'
    assert f(df1.a) == pytest.approx(0.0)
    assert f(df1.b) == pytest.approx(0.0)
    assert f(df1.c) == pytest.approx(2.5)
    assert f(df1.d) == pytest.approx(2.5)
    assert f(df1.e) == pytest.approx(0.22034017388059335)
    assert f(df1.f) == pytest.approx(0.6274205411570638)
    assert f(df1.g) == pytest.approx(12.0)


def test_percentile_df1(df1):
    f = percentile(25)
    assert f.__name__ == 'percentile_25'
    assert f(df1.a) == pytest.approx(0.0)
    assert f(df1.b) == pytest.approx(1.0)
    assert f(df1.c) == pytest.approx(3.25)
    assert f(df1.d) == pytest.approx(2.25)
    assert f(df1.e) == pytest.approx(0.27941244048295077)
    assert f(df1.f) == pytest.approx(-1.1127832698328843)
    assert f(df1.g) == pytest.approx(37.75)


def test_describe_numeric_1d_df1(df1):
    res = {c: describe_numeric_1d(df1[c]) for c in df1.columns if c != 'n'}

    # column a: all zeros
    assert list(res['a'].index) == describe_numeric_1d_expected_col_list
    assert res['a']['count'] == 10
    for c in ['1%', '5%', '25%', '50%', '75%', '95%', '99%', 'iqr', 'mad', 'mad_c1', 'max', 'mean', 'min', 'std']:
        assert res['a'][c] == pytest.approx(0.0)

    # column b: all ones
    assert list(res['b'].index) == describe_numeric_1d_expected_col_list
    assert res['b']['count'] == 10
    for c in ['1%', '5%', '25%', '50%', '75%', '95%', '99%', 'max', 'mean', 'min']:
        assert res['b'][c] == pytest.approx(1.0)
    for c in ['iqr', 'mad', 'mad_c1', 'std']:
        assert res['b'][c] == pytest.approx(0.0)

    # column c: 1 to 10
    assert list(res['c'].index) == describe_numeric_1d_expected_col_list
    assert res['c']['count'] == 10
    assert res['c']['mean'] == pytest.approx(5.5)
    assert res['c']['std'] == pytest.approx(3.027650)
    assert res['c']['mad'] == pytest.approx(3.706506)
    assert res['c']['mad_c1'] == pytest.approx(2.5)
    assert res['c']['iqr'] == pytest.approx(4.5)
    assert res['c']['min'] == pytest.approx(1.0)
    assert res['c']['1%'] == pytest.approx(1.09)
    assert res['c']['5%'] == pytest.approx(1.45)
    assert res['c']['25%'] == pytest.approx(3.25)
    assert res['c']['50%'] == pytest.approx(5.5)
    assert res['c']['75%'] == pytest.approx(7.75)
    assert res['c']['95%'] == pytest.approx(9.55)
    assert res['c']['99%'] == pytest.approx(9.91)
    assert res['c']['max'] == pytest.approx(10.0)


def test_describe_numeric_1d_empty_series():
    res = describe_numeric_1d(pd.Series())
    assert_array_equal(res.index, describe_numeric_1d_expected_col_list)
    for c in describe_numeric_1d_expected_col_list:
        if c == 'count':
            assert res[c] == 0
        else:
            assert np.isnan(res[c])
