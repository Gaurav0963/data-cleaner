import pandas as pd
import streamlit as st
from logger import logging as log
from exception import CustomException
from sklearn.model_selection import train_test_split
from pandas.api.types import is_numeric_dtype, is_object_dtype


def handle_missing_values(columns: list):
    '''### Helper Function : helps with filling missing values.
    ## Parameter
    columns : list of column(s) having missing values in them.
    ## Returns
    1. selected_column : column chosen for imputation.
    2. fill_method : method chosen for imputation.
    3. custom_val : value of imputation, if `custom` method is chosen.'''

    # We can only `fill missing values`, if there are columns with missing values present in the dataset. 
    if columns:
        try:
            numeric_columns, categorical_columns = get_column_dtype(st.session_state.df)
            selected_column = st.sidebar.selectbox("Select column", options=columns, index=None)
            # Object type columns don't have mean or medians
            if selected_column in categorical_columns:
                allowed_fill_methods = ['Custom','Forward Fill', 'Backward Fill', 'Mode']
            elif selected_column in numeric_columns:
                allowed_fill_methods = ['Custom','Forward Fill', 'Backward Fill', 'Mean', 'Median', 'Mode']
            fill_method = st.sidebar.selectbox("Select fill method", options=allowed_fill_methods, index=None)
            custom_val = None
            if fill_method == "Custom":
                custom_val = st.sidebar.text_input("Enter custom value: ")
            return selected_column, fill_method, custom_val
        except CustomException as ce:
            log.warning(f"{ce}")
    else:
        log.info('No Column with missing values!') 
        st.sidebar.markdown(":red[No Column with missing values!]")


def get_column_dtype(df: pd.DataFrame) -> list:
    '''This function checks whether the columns in a dataFrame are numeric or categorical.
    ## Parameters
    df : pandas.DataFrame
    ## Returns
    num_list, obj_list\n
    num_list : list containing numeric columns of DataFrame
    obj_list : list containing categorical columns of DataFrame'''
    num_list, obj_list = list(), list()
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            num_list.append(col)
        elif is_object_dtype(df[col]):
            obj_list.append(col)
    return num_list, obj_list


def get_columns_with_missing_values(df: pd.DataFrame|None) -> list|None:
    log.info("INSIDE get_columns_with_missing_values")
    '''## Returns
    list|None\n
    Returns a list columns having missing values in uploaded csv file.'''
    if df is not None:
        columns = df.columns[df.isnull().any()].tolist()
        log.info(f"Returning column list: {columns}")
        return columns
    log.info('DataFrame NOT found!, Returning None')
    return None

def split_df(df:pd.DataFrame, target):
    try:
        X = df.drop([target], axis=1)
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test
    except CustomException as ce:
        log.warning(f'{ce}')