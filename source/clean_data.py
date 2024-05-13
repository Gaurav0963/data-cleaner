import pandas as pd
import streamlit as st
from logger import logging as log

class CleanData:
    log.info("In class CleanData")
    '''This class performs basic cleaning operations which are performed on pandas DataFrame. The changes made are inplace, therefore, can't be reversed.
    Available functionality within the class are:
    1. Impute the columns having missing values
    2. Rename column
    3. Drop column(s) 
    '''
    def __init__(self, df)->None:
        self.df = df

    def fill_missing_values(self, column, method, custom=None)->None:
        log.info('INSIDE fill_missing_values')
        '''Imputes column having missing values with chosen method.
        ## Parameters
        column : column to be imputed.
        method : method used for calculation of value needed for imputation.
        custom : (provided by user) custom value a column is to be imputed with.
        ## Returns
        str & numeric_value | str & None\n
        1. Code : returns auto-generated code to the imputation.
        2. Value : returns value with which missing data is filled with (if applicable) or None.'''
        try:
            if self.df is not None and column:
                value = None
                log.info(f"method chosen: {method}")
                if method == 'Forward Fill':
                    code = f"df['{column}'] = df['{column}'].ffill()"
                    self.df[column] = self.df[column].ffill()
                elif method == 'Backward Fill':
                    self.df[column] = self.df[column].bfill()
                    code = f"df['{column}'] = df['{column}'].ffill()"
                else:
                    fill_methods = {
                    'Custom': custom,
                    'Mean': round(self.df[column].mean(), 2),
                    'Median': self.df[column].median(),
                    'Mode': self.df[column].mode().iloc[0]
                    }
                    self.df.fillna({column: fill_methods[method]}, inplace=True)
                    value = fill_methods[method]
                    if method == 'Custom':
                        code = f"# Using custom value = {custom} to fill missing values\n"
                    else:
                        code = f"{method} = df['{column}'].{method}()\n"
                    code += f"df.fillna('{{{column}:{fill_methods[method]}}}', inplace=True)"
                log.info(f"Returning code and value")
                return code, value
        except Exception as e:
            log.warning(f"{e}")
            st.warning(e)

    def change_column_name(self, old_name, new_name)->str:
        log.info('INSIDE change_column_name')
        '''Rename column.
        ## Parameters
        old_name : column name, to be renamed.
        new_came : New column name
        ## Returns
        code (str) : returns auto-generated code to rename a column
        '''
        if self.df is not None:
            self.df.rename(columns={old_name: new_name}, inplace=True)
            code = f"df.rename(columns={{'{old_name}': '{new_name}'}}, inplace=True)\n"
            code += f"# or use the following code instead\n"
            code += f"# df.columns = df.columns.str.replace('{old_name}', '{new_name}')"
        log.info(f"Returning code")
        return code
    
    def drop_column(self, column_to_drop)->str:
        log.info('INSIDE drop_column')
        '''Drops the column.
        ## Parameter
        column_to_drop : Name of the column to be dropped.
        ## Returns
        code (str): auto generated code to drop a column.
        '''
        if self.df is not None and column_to_drop:
            try:
                self.df = self.df.drop(columns=column_to_drop, inplace=True)
                code = f"df.drop(columns={column_to_drop}, inplace=True)"
                return code
            except Exception as e:
                log.warning(f"{e}")
                pass     

    # This function let's user make dynamic change in DataFrame,
    # and stores the keys as modified rows in session_state.
    def df_on_change(self, df)->None:
        state = st.session_state["df_editor"]
        for index, updates in state["edited_rows"].items():
            for key, value in updates.items():
                self.df.loc[index, key] = value

    def editor(self)->None:
        if "df" not in st.session_state:
            st.session_state["df"] = self.df
        st.data_editor(st.session_state["df"], key="df_editor", on_change=self.df_on_change, args=[self.df])