import pandas as pd
import streamlit as st
from clean_data import CleanData
from encode_data import EncodeData
from logger import logging as log
from utils import get_column_dtype

def Fill_missing_values(columns_with_missing_values):
    # We can only `fill missing values`, if there are columns with missing values present in the dataset. 
    if columns_with_missing_values:
        try:
            numeric_columns, categorical_columns = get_column_dtype(st.session_state.df)
            selected_column = st.sidebar.selectbox("Select column", options=columns_with_missing_values, index=None)
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
        except:...
    else:
        log.info('No Column with missing values!') 
        st.sidebar.markdown(":red[No Column with missing values!]")


def main():
    log.info("Inside main()")
    st.title("CSV Processor")
    # Initialising Class CleanData object with uploaded DataFrame*
    cln = CleanData(st.session_state.df)

    st.write(f"{st.session_state.name}")
    cln.editor()

    # Hack to update Original CSV file, reruns the script.
    if st.button("Update File"):
        log.info(f"`Update File` Button Clicked :heavy_check_mark")

    # Short summary of dataFrame, so that informed descisions can be made about the data.
    if st.toggle(":blue[Show Data Summary]"):
        log.info("Show Data Summary, Toggled switch")
        st.write(f"Rows: {st.session_state.df.index.size}, Columns: {st.session_state.df.columns.size}")
        if columns_with_missing_values:
            st.write("Columns with missing values:", columns_with_missing_values)
        else:
            st.write("No columns with missing values")
        st.write("Total Duplicate Rows : ", st.session_state.df.duplicated().sum())

    # Choose from data-cleaning processes.
    select_opt = ["Fill Missing Values", "Rename Column", "Drop Column", "Drop Duplicate Rows"]
    selectbox = st.sidebar.selectbox(label="Select Process", options=select_opt, index=None)

    # IMPUTE MISSING VALUES
    if selectbox == "Fill Missing Values":
        log.info(f"Select Process: {selectbox}")
        columns_with_missing_values = cln.get_columns_with_missing_values()
        try:
            selected_column, fill_method, custom_val = Fill_missing_values(columns_with_missing_values)
            if  (selected_column and fill_method!='Custom' and fill_method!=None) or (selected_column and fill_method=='Custom' and custom_val):
                if st.sidebar.button("Impute Values"):
                    log.info(f"`Impute Values`, button clicked")
                    generated_code, value_filled = cln.fill_missing_values(selected_column, fill_method, custom=custom_val)
                    if value_filled:
                        st.write(f"Missing values filled in '{selected_column}' using {fill_method} : {value_filled}")
                    else:
                        st.write(f"Missing value filled in '{selected_column}' using {fill_method}")   
                    st.write("Python Code for filling missing values:")
                    st.code(generated_code)
                    st.write("Modified CSV:")
                    st.write(st.session_state.df)
        except: st.sidebar.markdown(":red[!]")

    # CHANGE COLUMN NAME
    if selectbox == "Rename Column":
        log.info(f"Select Process: {selectbox}")
        try:
            selected_column = st.sidebar.selectbox("Select column", options=st.session_state.df.columns, index=None)
            new_column_name = st.sidebar.text_input("Enter new name for the column")
            if selected_column and new_column_name:
                log.info(f"Old column name: {selected_column}, New column name: {new_column_name}")
                if st.sidebar.button("Update Name"):
                    log.info("`Update Name`, button clicked")
                    code_for_rename = cln.change_column_name(selected_column, new_column_name)
                    st.write("Column name changed from", selected_column, "to", new_column_name)
                    st.write("Python Code for changing column name:")
                    st.code(code_for_rename)
                    st.write("Modified CSV:")
                    st.write(st.session_state.df)
        except:...

    # DROP COLUMNS
    if selectbox == "Drop Column":
        log.info(f"Select Process: {selectbox}")
        column_to_drop = st.sidebar.multiselect("Select column", options=st.session_state.df.columns.tolist())
        if column_to_drop is not None: # this way 'Drop' button doesn't show until column is chosen
            log.info(f"Columns to drop: {column_to_drop}")
            if st.sidebar.button("Drop"):
                log.info("`Drop`, button clicked")
                code_drop = cln.drop_column(column_to_drop)
                st.write("Column", column_to_drop, "dropped")
                st.write("Python Code for dropping column:")
                st.code(code_drop)
                st.write("Modified CSV:")
                st.write(st.session_state.df)

    # HANDLE DUPLICATE ROWS
    if selectbox == "Drop Duplicate Rows":
        log.info(f"Select Process: {selectbox}")
        duplicates = st.session_state.df.duplicated().sum()
        if duplicates > 0 and st.sidebar.button(f"Drop {duplicates} Duplicate Rows", duplicates):
            log.info(f"{duplicates} duplicates dropped!!")
            st.session_state.df.drop_duplicates(inplace=True)
            st.write(f"df.drop_duplicates(inplace=True)")
        elif duplicates == 0:
            log.info('Duplocate rows not found.')
            st.sidebar.markdown(":red[***No duplicate rows available!***]")
            

if __name__ == "__main__":
    main()
