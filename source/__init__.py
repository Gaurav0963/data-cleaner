import streamlit as st
import pandas as pd


# Function to load data and save to session state
@st.cache_data(experimental_allow_widgets=True)
def load_data(file):
    return pd.read_csv(file)

def main():
    st.title(":red[Load Data]")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Creating a session
        # if 'df' not in st.session_state:
        st.session_state.df = load_data(uploaded_file)
        # if 'name' not in st.session_state:
        st.session_state.name = uploaded_file.name

        st.warning(":red[progress might be lost]")

if __name__ == "__main__":
    main()
