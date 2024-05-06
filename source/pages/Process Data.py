import streamlit as st
import pandas as pd


class CSVProcessor:
    def __init__(self, df):
        self.df = df

    def get_columns_with_missing_values(self):
        if self.df is not None:
            return self.df.columns[self.df.isnull().any()].tolist()
        return None

    def fill_missing_values(self, selected_column, method, custom=None):
        if self.df is not None and selected_column:
            value = None
            if method == 'Custom':
                self.df[selected_column] = self.df[selected_column].fillna(custom)
                code = f"df.['{selected_column}'] = df['{selected_column}'].fillna({custom})"
                value = custom
            elif method == 'Forward Fill':
                self.df[selected_column].fillna(method='ffill', inplace=True)
                code = f"df['{selected_column}'].fillna(method='ffill', inplace=True)"
            elif method == 'Backward Fill':
                self.df[selected_column].fillna(method='bfill', inplace=True)
                code = f"df['{selected_column}'].fillna(method='bfill', inplace=True)"
            elif method == 'Mean':
                value = self.df[selected_column].mean()
                self.df[selected_column].fillna(value, inplace=True)
                code = f"mean_value = df['{selected_column}'].mean()\n"
                code += f"df['{selected_column}'].fillna(mean_value, inplace=True)"
            elif method == 'Median':
                value = self.df[selected_column].median()
                self.df[selected_column].fillna(value, inplace=True)
                code = f"median_value = df['{selected_column}'].median()\n"
                code += f"df['{selected_column}'].fillna(median_value, inplace=True)"
            elif method == 'Mode':
                value = self.df[selected_column].mode().iloc[0]
                self.df[selected_column].fillna(value, inplace=True)
                code = f"mode_value = df['{selected_column}'].mode().iloc[0]\n"
                code += f"df['{selected_column}'].fillna(mode_value, inplace=True)"
        return code, value

    def change_column_name(self, old_name, new_name):
        if self.df is not None:
            self.df.rename(columns={old_name: new_name}, inplace=True)
            code = f"df.rename(columns={{'{old_name}': '{new_name}'}}, inplace=True)\n"
            code += f"# or use the following code instead\n"
            code += f"# df.columns = df.columns.str.replace('{old_name}', '{new_name}')"
        return code
    
    def drop_column(self, column_to_drop):
        if self.df is not None and column_to_drop:
            self.df = self.df.drop(columns=[column_to_drop], axis=1, inplace = True)
            code = f"df.drop(columns=['{column_to_drop}'], inplace=True)"
            return code        

    # This function let's user make dynamic change in DataFrame.
    def df_on_change(self, df):
        state = st.session_state["df_editor"]
        for index, updates in state["edited_rows"].items():
            for key, value in updates.items():
                self.df.loc[index, key] = value

    def editor(self):
        if "df" not in st.session_state:
            st.session_state["df"] = self.df
        st.data_editor(st.session_state["df"], key="df_editor", on_change=self.df_on_change, args=[self.df])


def main():
    st.title("CSV Processor")

    obj = CSVProcessor(st.session_state.df)

    st.write(f"{st.session_state.name}")
    obj.editor()

    # Hack to update Original CSV file, reruns the script.
    if st.button("Update File"):...

    columns_with_missing_values = obj.get_columns_with_missing_values()

    # Short summary of dataFrame, so that informed descisions can be made about the data.
    if st.toggle(":blue[Show Data Summary]"):
        st.write(f"Rows: {st.session_state.df.index.size}, Columns: {st.session_state.df.columns.size}")
        if columns_with_missing_values:
            st.write("Columns with missing values:", columns_with_missing_values)
        else:
            st.write("No columns with missing values")
        st.write("Total Duplicate Rows : ", st.session_state.df.duplicated().sum())

    # Choose from data-cleaning processes.
    select_opt = ["Fill Missing Values", "Change Column Name", "Drop Column", "Drop Duplicates"]
    selectbox = st.sidebar.selectbox(label="Select Process", options=select_opt, index=None)
    
    # IMPUTE MISSING VALUES
    # We can only `fill missing values`, if there are columns with missing values present in the dataset. 
    if selectbox == "Fill Missing Values":
        if columns_with_missing_values:
            try:
                selected_column = st.sidebar.selectbox("Select column", options=columns_with_missing_values, index=None)

                # Object type columns don't have mean or medians
                if st.session_state.df[selected_column].dtype == 'object':
                    allowed_fill_methods = ['Custom','Forward Fill', 'Backward Fill', 'Mode']
                else:
                    allowed_fill_methods = ['Custom','Forward Fill', 'Backward Fill', 'Mean', 'Median', 'Mode']
                
                fill_method = st.sidebar.selectbox("Select fill method", options=allowed_fill_methods, index=None)

                custom_val = None
                if fill_method == "Custom":
                    custom_val = st.sidebar.text_input("Enter custom value: ")

                # This condition ensures that the button "Impute Values" is only shown iff:
                #   1. The selected column is not None.
                #   2. If the fill method is not "Custom" and not None.
                #   3. Or if the fill method is "Custom" and a custom value is provided.
                if  (selected_column and fill_method!='Custom' and fill_method!=None) or (selected_column and fill_method=='Custom' and custom_val):
                    if st.sidebar.button("Impute Values"):
                        code_fill, value_filled = obj.fill_missing_values(selected_column, fill_method, custom=custom_val)
                        if value_filled:
                            st.write(f"Missing values filled in '{selected_column}' using {fill_method} : {value_filled}")
                        else:
                            st.write(f"Missing value filled in '{selected_column}' using {fill_method}")   
                        st.write("Python Code for filling missing values:")
                        st.code(code_fill)
                        st.write("Modified CSV:")
                        st.write(st.session_state.df)
            except:...
        else: st.sidebar.markdown(":red[No Column with missing values!]")
        

    # CHANGE COLUMN NAME
    if selectbox == "Change Column Name":
        try:
            selected_column = st.sidebar.selectbox("Select column", options=st.session_state.df.columns, index=None)
            new_column_name = st.sidebar.text_input("Enter new name for the column")
            if new_column_name:
                if st.sidebar.button("Update Name") and new_column_name:
                    code_rename = obj.change_column_name(selected_column, new_column_name)
                    st.write("Column name changed from", selected_column, "to", new_column_name)
                    st.write("Python Code for changing column name:")
                    st.code(code_rename)
                    st.write("Modified CSV:")
                    st.write(st.session_state.df)
        except:...

    # DROP COLUMNS
    if selectbox == "Drop Column":
        column_to_drop = st.sidebar.multiselect("Select column", options=st.session_state.df.columns.tolist())
        if column_to_drop is not None: # this way 'Drop' button doesn't show until column is chosen
            if st.sidebar.button("Drop"):
                code_drop = obj.drop_column(column_to_drop)
                st.write("Column", column_to_drop, "dropped")
                st.write("Python Code for dropping column:")
                st.code(code_drop)
                st.write("Modified CSV:")
                st.write(st.session_state.df)

    # HANDLE DUPLICATE ROWS
    if selectbox == "Drop Duplicates":
        duplicates = st.session_state.df.duplicated().sum()
        if duplicates > 0 and st.sidebar.button(f"Drop {duplicates} Duplicate Rows",duplicates):
            st.session_state.df.drop_duplicates(inplace=True)
            st.write(f"df.drop_duplicates(inplace=True)")
        elif duplicates == 0:
            st.sidebar.markdown(":red[***No duplicate rows available!***]")
                

if __name__ == "__main__":
    main()
