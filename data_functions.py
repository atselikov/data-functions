import pandas as pd

def drop_corr_columns(df, drop_columns=True, print_columns=True, threshold=0.98):
    """
    Usually removing high correlated columns gives improvement in model's quality.
    The task of this function:
        1. Print list of the most correlated columns
        2. Remove them by threshold

    Parameters
    ----------
    df : pandas dataframe

    drop_columns : Boolean

    print_columns : Boolean

    threshold: shold be in [0.7 ... 1]
        A threshold value to drop correlated columns

    Returns
    -------
    df : pandas dataframe

    See Also
    --------
    pandas.DataFrame.corr description:  https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html

    Notes
    -----

    Examples
    --------
    # Just check for correlated columns:
    df = drop_corr_columns(df, drop_columns=False, print_columns=True, threshold=0.85)
    """

    # 1. calculation
    CorrCoeff = df.corr()

    # 2. report
    CorrFieldsList = []
    print('Columns with correlations more than %s :' % str(threshold))
    for i in CorrCoeff:
        for j in CorrCoeff.index[CorrCoeff[i] >= threshold]:
            if i != j and j not in CorrFieldsList:
                CorrFieldsList.append(j)
                if print_columns:
                    print("%s-->%s: r^2=%f" % (i, j, CorrCoeff[i][CorrCoeff.index == j].values[0]))
    #print()
    #print('Correlated columns count: %', len(CorrFieldsList))

    # 3. dropping
    if drop_columns:
        print('%s columns total' % df.shape[1])
        df = df.drop(CorrFieldsList, 1)
        print('%s columns left' % df.shape[1])

    return df

def drop_const_columns(df, drop_columns=True, print_columns=True):
    """
    Usually removing constant columns gives improvement in model's quality.
    The task of this function:
        1. Print list of constant columns
        2. Drop them by threshold

    Parameters
    ----------
    df : pandas dataframe

    drop_columns : Boolean

    print_columns : Boolean

    Returns
    -------
    df : pandas dataframe

    See Also
    --------

    Notes
    -----

    Examples
    --------
    # Just check for constant columns:
    df = drop_const_columns(df, drop_columns=False, print_columns=True)
    """



    # 1. report

    SingleValueCols = []
    for col in df.columns:
        unique_count=df[col].nunique()
        if unique_count < 2:
            SingleValueCols.append(col)
            if print_columns:
                print(col, unique_count)

    print
    print('Constant columns count: %s' % len(SingleValueCols))

    # 2. dropping
    if drop_columns:
        print('%s columns total' % df.shape[1])
        df = df.drop(SingleValueCols, 1)
        print('%s columns left' % df.shape[1])

    return df


def find_date_columns(df):
    """
        1. Find date columns automatically
        2. Convert them to datetime format

    Parameters
    ----------
    df : pandas dataframe

    Returns
    -------
    df : pandas dataframe

    See Also
    --------

    Notes
    -----

    Examples
    --------
    #
    df = find_date_columns(df)
    """

    def look_to_date(s):
        dates = {date: pd.to_datetime(date) for date in s.unique()}
        return s.apply(lambda v: dates[v])

    date_cols = []
    for col in df.select_dtypes(include=['object']).columns:
        try:
            df[col] = look_to_date(df[col])
            print(col)
            date_cols.append(col)
        except ValueError:
            pass
    return df