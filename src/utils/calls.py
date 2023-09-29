from typing import Union
import pandas as pd
#calling companies from similar industries based on company ID.
def call_industry(mother_df: pd.DataFrame,ciiu_df: pd.DataFrame,ruc: Union[str,int]) -> pd.DataFrame:
    ciiu_str = ciiu_df.query(f"ruc == '{str(ruc)}'")["ciiu"].values[0]
    #Filter mother_df by companies that belong to the same industry as company input in args.
    mother_df = (
        mother_df
        .merge(right = ciiu_df,how = "inner", on = "ruc")
        .set_index(["ruc","codigo"])
        .query(f"ciiu == '{ciiu_str}'")
        .drop("ciiu",axis = 1)
    )
    return mother_df

#calling a specific company from the database
def call_company(mother_df: pd.DataFrame,ruc: str):
    df_company = mother_df.query(f"ruc == '{ruc}'")
    return df_company
