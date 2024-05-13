import utils
import pandas as pd
import streamlit as st
from clean_data import CleanData
from logger import logging as log
from encode_data import EncodeData
from exception import CustomException
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Process Data",
    page_icon=":material/display_settings:"
)

def impute_values(cls_obj, columns_na) -> None:
    try:
        # selected_column, fill_method, custom_val = Fill_missing_values(columns_with_missing_values)
        selected_column, fill_method, custom_val = utils.handle_missing_values(columns_na)
        if  (selected_column and fill_method!='Custom' and fill_method!=None) or (selected_column and fill_method=='Custom' and custom_val):
            if st.sidebar.button("Impute Values"):
                log.info(f"`Impute Values`, button clicked")
                generated_code, value_filled = cls_obj.fill_missing_values(selected_column, fill_method, custom=custom_val)
                if value_filled:
                    st.write(f"Missing values filled in '{selected_column}' using {fill_method} : {value_filled}")
                else:
                    st.write(f"Missing value filled in '{selected_column}' using {fill_method}")   
                st.write("Python Code for filling missing values:")
                st.code(generated_code)
                st.write("Modified CSV:")
                st.write(st.session_state.df)
    except: st.sidebar.markdown(":red[!]")

def rename(cls_obj) -> None:
    try:
        selected_column = st.sidebar.selectbox("Select column", options=st.session_state.df.columns, index=None)
        new_column_name = st.sidebar.text_input("Enter new name for the column")
        if selected_column and new_column_name:
            log.info(f"Old column name: {selected_column}, New column name: {new_column_name}")
            if st.sidebar.button("Update Name"):
                log.info("`Update Name`, button clicked")
                code_for_rename = cls_obj.change_column_name(selected_column, new_column_name)
                st.write("Column name changed from", selected_column, "to", new_column_name)
                st.write("Python Code for changing column name:")
                st.code(code_for_rename)
                st.write("Modified CSV:")
                st.write(st.session_state.df)
    except:...

def drop(cls_obj) -> None:
    column_to_drop = st.sidebar.multiselect("Select column", options=st.session_state.df.columns.tolist())
    if column_to_drop is not None: # this way 'Drop' button doesn't show until column is chosen
        log.info(f"Columns to drop: {column_to_drop}")
        if st.sidebar.button("Drop"):
            log.info("`Drop`, button clicked")
            code_drop = cls_obj.drop_column(column_to_drop)
            st.write("Column", column_to_drop, "dropped")
            st.write("Python Code for dropping column:")
            st.code(code_drop)
            st.write("Modified CSV:")
            st.write(st.session_state.df)

def drop_duplicates() -> None:
    duplicates = st.session_state.df.duplicated().sum()
    if duplicates > 0 and st.sidebar.button(f"Drop {duplicates} Duplicate Rows", duplicates):
        log.info(f"{duplicates} duplicates dropped!!")
        st.session_state.df.drop_duplicates(inplace=True)
        st.write(f"df.drop_duplicates(inplace=True)")
    elif duplicates == 0:
        log.info('Duplocate rows not found.')
        st.sidebar.markdown(":red[***No duplicate rows available!***]")

def data_summary(columns_with_missing_values) -> None:
    st.write(f"Rows: {st.session_state.df.index.size}, Columns: {st.session_state.df.columns.size}")
    if columns_with_missing_values:
        st.write("Columns with missing values:", columns_with_missing_values)
    else:
        st.write("No columns with missing values")
    st.write("Total Duplicate Rows : ", st.session_state.df.duplicated().sum())


def clean():
    try:
        log.info("Inside main()")
        st.title(":red[CSV Processor]")
        # Initialising Class CleanData object with uploaded DataFrame*
        clean_data = CleanData(st.session_state.df)

        st.write(f":red[{st.session_state.name}]")
        clean_data.editor()

        # Hack to update Original CSV file, reruns the script.
        if st.button("Update File"):
            log.info(f"`Update File` Button Clicked ")

        # columns_with_missing_values = clean_data.get_columns_with_missing_values()
        columns_with_missing_values = utils.get_columns_with_missing_values(st.session_state.df)
        
        # Short summary of dataFrame, so that informed descisions can be made about the data.
        if st.toggle(":red[Show Data Summary]"):
            log.info("Show Data Summary, Toggled switch")
            data_summary(columns_with_missing_values)

        # Choose from data-cleaning processes.
        select_opt = ["Fill Missing Values", "Rename Column", "Drop Column", "Drop Duplicate Rows"]
        selectbox = st.sidebar.selectbox(label="Select Process", options=select_opt, index=None)

        # IMPUTE MISSING VALUES
        if selectbox == "Fill Missing Values":
            log.info(f"Select Process: {selectbox}")
            impute_values(cls_obj=clean_data, columns_na=columns_with_missing_values)

        # CHANGE COLUMN NAME
        if selectbox == "Rename Column":
            log.info(f"Select Process: {selectbox}")
            rename(cls_obj=clean_data)

        # DROP COLUMNS
        if selectbox == "Drop Column":
            log.info(f"Select Process: {selectbox}")
            drop(cls_obj=clean_data)

        # HANDLE DUPLICATE ROWS
        if selectbox == "Drop Duplicate Rows":
            log.info(f"Select Process: {selectbox}")
            drop_duplicates()

    except AttributeError:
        st.page_link("Load_Data.py", label="Load Data", icon="⬆️")
        st.warning(':red[Please load data by clicking on the link above!]')


def encode():
    try:
        columns = st.session_state.df.columns.to_list()
        target = st.sidebar.selectbox(f"Splitting DataFrame; Select target column", options=columns, index=None)
        if target:
            X_train, X_test, y_train, y_test = utils.split_df(st.session_state.df, target)
            enc = EncodeData(X_train, X_test)
            enc_X_train, enc_X_test=enc.OHE()
            st.data_editor(enc_X_train)
                
    except AttributeError:
        st.page_link("Load_Data.py", label="Load Data", icon="⬆️")
        st.warning(f":red[Data not found!]")


if __name__ == "__main__":
    selected = option_menu(
        menu_title=None,
        options=['Clean', 'Encode'],
        default_index=0,
        orientation='horizontal',
    )

    if selected == 'Clean': clean()

    elif selected == 'Encode': encode()
