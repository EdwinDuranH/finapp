import numpy as np
import pandas as pd

from typing import Optional
import zipfile


# utility functions
def check_name(colname: str) -> bool:
    """Check if a column name is a number, if so, return True"""
    try:
        int(colname)
        return True
    except ValueError:
        return False


def check_negative(df: pd.DataFrame) -> pd.DataFrame:
    """
    Check if the 'valor' column has negative values, if not, multiply by -1

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe must contain 'valor' column
    """
    # assert 'valor' exists, otherwise raise error
    assert all(c in df.columns for c in [
               'cuenta', 'valor', 'codigo']), "Column 'valor' must be in df"

    # redefine the 'valor' column correcting for values that should be negative
    cond = (df['cuenta'].str.contains('(-)', regex=False)) & (df['valor'] > 0)
    _valor = df.valor.mask(cond, other=df.valor.mul(-1))
    return df.assign(valor=_valor)


def recursive_agg(df: pd.DataFrame, account: str) -> float:
    """Add all children accounts of a given account, considering also the children of the children\
        to ensure consistency."""

    assert all(c in df.columns for c in [
               'valor', 'codigo']), "Column 'valor' must be in df"

    account = str(account)

    # subset data for immediate children
    cond = (df['codigo'].str.startswith(account)) & \
        (df['codigo'].str.len() == len(account) + 2)
    children = df[cond]

    # recursive addition of children accounts
    if children.empty:
        return df[df['codigo'] == account].valor.sum()
    else:
        children_sum = 0
        for child in children['codigo'].values:
            children_sum += recursive_agg(df, child)

        # Adjust equity account to incluse account 31, a even numbered account. An anomaly.
        if account == str(3):
            children_sum += df[df['codigo'] == '31'].valor.sum()

        return round(children_sum, ndigits=2)


def read_member(z_path: str, file: str, **kwargs) -> pd.DataFrame:
    """
    Read in a file from a zip archive.

    Parameters
    ----------
    z_path : str
        Path to the zip archive.
    file : str
        Name of the file to read in.
    """
    with zipfile.ZipFile(z_path, mode='r') as z:
        with z.open(file, mode='r') as zout:
            df = pd.read_csv(zout,
                             sep='\t',
                             encoding='latin1',
                             **kwargs)
    return df
