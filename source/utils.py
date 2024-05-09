import pandas as pd
from pandas.api.types import is_numeric_dtype, is_object_dtype

def handle_missing_values(columns):...

def get_column_dtype(df: pd.DataFrame) -> list:
    '''This function checks whether the columns in a dataFrame are numeric or categorical.
    ## Parameters
    df : pandas.DataFrame

    ## Returns
    num_list, obj_list
    
    num_list : list containing numeric columns of DataFrame
    obj_list : list containing categorical columns of DataFrame
    '''
    num_list, obj_list = list(), list()
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            num_list.append(col)
        elif is_object_dtype(df[col]):
            obj_list.append(col)
    return num_list, obj_list