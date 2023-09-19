import pandas as pd

from typing import Optional

from utils.preprocessing import read_member, check_name


def preProcessor(df: pd.DataFrame, filename: Optional[str] = None, meta: Optional[pd.DataFrame] = None) -> None:
    """
    Transform the raw data into a tidy format, and save it to a csv file.
    """
    filename = 'balances2022.csv'
    filename_ids = 'balaces2022_ids.csv'

    df_data = (df
               .rename(lambda c: c.lower().replace('cuenta_', ''), axis=1)
               .pipe(lambda df_: df_.drop(columns=[c for c in df_.columns
                                                   if not check_name(c) and 'ruc' not in c]))
               .melt(id_vars='ruc', var_name='codigo', value_name='valor')
               .sort_values(by=['ruc', 'codigo'])
               .assign(valor=lambda df_: df_.valor.str.replace(',', '.').astype(float))
               .set_index(['ruc', 'codigo'])
               )

    df_ids = (df
              .iloc[:, :7]
              .rename(lambda c: c.lower(), axis=1)
              .drop(columns=['expediente'])
              .set_index('ruc')
              )

    for df_, fname in zip(
        [df_data, df_ids],
        [filename, filename_ids]
    ):
        df_.to_csv(f'../data/processed/{fname}', index=True)

    if meta is not None:
        meta.to_csv('../data/processed/balances2022_meta.csv', index=True)


if __name__ == "__main__":
    df = read_member(z_path='../data/raw/estadosFinancieros_2022.zip',
                     file='balances_2022_1.txt')

    meta = read_member(z_path='../data/raw/estadosFinancieros_2022.zip',
                       file='catalogo_2022_1.txt',
                       names=['codigo', 'cuenta'],
                       index_col='codigo')

    # run preProcessor routine
    preProcessor(df=df, meta=meta)
