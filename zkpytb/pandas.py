"""
Small helper functions related to pandas functionalities

Author: Marc Gallet (2017)
"""

import numpy as np
import pandas as pd


# More percentiles when using pd.describe()
extended_percentiles = [.01, .05, .25, .5, .75, .95, .99]


def tdescr(df_in, percentiles=None, disp=True):
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


def df_query_with_ratio(df_in, query, ratio_name='ratio'):
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


def remove_outliers(df_in, column, sigma=3):
    """
    Very simple filter that removes outlier rows
    from a DataFrame based on the distance from the
    mean value measured in standard deviations.
    """
    return df_in[np.abs(df_in[column] - df_in[column].mean()) <= (sigma * df_in[column].std())]


def only_outliers(df_in, column, sigma=3):
    """
    Very simple filter that only keeps outlier rows
    from a DataFrame based on the distance from the
    mean value measured in standard deviations.
    """
    return df_in[np.abs(df_in[column] - df_in[column].mean()) > (sigma * df_in[column].std())]


def move_col_to_beginning_of_df(df_in, colname):
    """
    Small helper to move a column to the beginning of the DataFrame
    """
    cols = df_in.columns.tolist()
    cols.insert(0, cols.pop(cols.index(colname)))
    return df_in.reindex(columns=cols)


def compare_df_cols(df_list, col_list, mode=1):
    """
    Helper to compare the values of common columns between different dataframes

    Mode 1: iterate over columns as top level and DataFrames as second level
    Mode 2: iterate over DataFrames as top level and columns as second level
    """
    if mode == 1:
        colstoconcat = [df.loc[col].rename(df.loc[col].name + '_' + str(i + 1))
                        for col in col_list
                        for i, df in enumerate(df_list)]
    elif mode == 2:
        colstoconcat = [df.loc[col].rename(df.loc[col].name + '_' + str(i + 1))
                        for i, df in enumerate(df_list)
                        for col in col_list]
    else:
        return None

    return pd.concat(colstoconcat, axis=1)
