"""
Small helper functions related to pandas functionalities

Author: Marc Gallet (2017)
"""

from typing import List, Optional, Tuple

try:
    import numpy as np
    import pandas as pd
    import scipy
except ImportError:  # pragma: no cover
    raise ImportError(
        'numpy, pandas and scipy packages are required in order to use this module '
        'but they will not installed automatically by the zkpytb package. '
        'Please install them yourself.'
    )


# More percentiles when using pd.describe()
extended_percentiles: List[float] = [.01, .05, .25, .5, .75, .95, .99]


def tdescr(df_in: pd.DataFrame,
           percentiles: Optional[List[float]] = None,
           disp: bool = True) -> pd.DataFrame:
    """
    Helper function to display and return the transposition
    of the output of DataFrame.describe(). This means that
    the columns of the input DataFrame are returned as rows
    and the various statistical values of interest are the
    columns in the result.

    It is useful when the input dataframe has a lot of columns.

    This function additionally computes the statistics on a
    larger set of percentiles than the default DataFrame.describe()
    function.
    """
    try:
        from IPython.display import display
    except ImportError:
        display = print

    if not percentiles:
        percentiles = [.01, .05, .25, .5, .75, .95, .99]

    tdescr_out = df_in.describe(percentiles).T
    if disp:
        display(tdescr_out)
    return tdescr_out


def df_query_with_ratio(df_in: pd.DataFrame, query: str, ratio_name='ratio') -> Tuple[pd.DataFrame, float]:
    """
    This function calls the .query() method on a DataFrame
    and additionally computes the ratio of resulting rows
    over the original number of rows.

    The result is a tuple with the filtered dataframe as first
    element and the filter ratio as second element.
    """
    df_out = df_in.query(query)
    ratio = df_out.shape[0] / df_in.shape[0]
    print('{} = {:.2f} %'.format(ratio_name, 100 * ratio))
    return df_out, ratio


def remove_outliers(df_in: pd.DataFrame, column, sigma: float = 3) -> pd.DataFrame:
    """
    Very simple filter that removes outlier rows
    from a DataFrame based on the distance from the
    mean value measured in standard deviations.
    """
    return df_in[np.abs(df_in[column] - df_in[column].mean()) <= (sigma * df_in[column].std())]


def only_outliers(df_in: pd.DataFrame, column, sigma: float = 3) -> pd.DataFrame:
    """
    Very simple filter that only keeps outlier rows
    from a DataFrame based on the distance from the
    mean value measured in standard deviations.
    """
    return df_in[np.abs(df_in[column] - df_in[column].mean()) > (sigma * df_in[column].std())]


def move_col_to_beginning_of_df(df_in: pd.DataFrame, colname: str) -> pd.DataFrame:
    """
    Small helper to move a column to the beginning of the DataFrame
    """
    cols = df_in.columns.tolist()
    cols.insert(0, cols.pop(cols.index(colname)))
    return df_in.reindex(columns=cols)


def compare_df_cols(df_list: List[pd.DataFrame], col_list: List[str], mode=1) -> Optional[pd.DataFrame]:
    """
    Helper to compare the values of common columns between different dataframes

    Mode 1: iterate over columns as top level and DataFrames as second level
    Mode 2: iterate over DataFrames as top level and columns as second level
    """
    if mode == 1:
        colstoconcat = [df.loc[:, col].rename(str(df.loc[:, col].name) + '_' + str(i + 1))
                        for col in col_list
                        for i, df in enumerate(df_list)]
    elif mode == 2:
        colstoconcat = [df.loc[:, col].rename(str(df.loc[:, col].name) + '_' + str(i + 1))
                        for i, df in enumerate(df_list)
                        for col in col_list]
    else:
        return None

    return pd.concat(colstoconcat, axis=1)


def mad(c=None, name='mad'):
    try:
        import statsmodels.robust as smrb
    except ImportError:  # pragma: no cover
        raise ImportError(
            'The statsmodels package is required in order to use this function '
            'but it will not installed automatically by the zkpytb package. '
            'Please install it yourself.'
        )

    if c is not None:
        def _mad(x):
            return smrb.mad(x, c=c)
    else:
        def _mad(x):
            return smrb.mad(x)
    _mad.__name__ = name
    return _mad


def percentile(n):

    def _percentile(x):
        return np.percentile(x, n)
    _percentile.__name__ = 'percentile_%02d' % n

    return _percentile


def describe_numeric_1d(series: pd.Series):
    """
    Patched version of pandas' .describe() function for Series
    which includes the calculation of the median absolute deviation and interquartile range

    If the input Series is empty, the returned Series has "count" == 0
    and all other stats are set to np.nan
    """
    stat_index = (['count', 'mean', 'std', 'mad', 'mad_c1', 'iqr', 'min']
                  + pd.io.formats.format.format_percentiles(extended_percentiles) + ['max'])  # type: ignore
    if series.empty:
        # [0, np.nan, np.nan, ..., np.nan]
        d = [0] + [np.nan] * (len(stat_index) - 1)
    else:
        d = (
            [
                series.count(),
                series.mean(),
                series.std(),
                mad()(series.dropna()),
                mad(1, name='mad_c1')(series.dropna()),
                scipy.stats.iqr(series, nan_policy='omit'),
                series.min()
            ]
            + series.quantile(extended_percentiles).tolist()
            + [series.max()]
        )
    return pd.Series(d, index=stat_index, name=series.name)
