import streamlit as st
import pandas as pd


# Function to load data and save to session state
@st.cache_data(experimental_allow_widgets=True)
def load_data(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error reading data: {e}")

def create_session(file) -> None:
    '''This function creates a new session to be used throughout the app.
    :params file: uploaded file object
    :return: None
    '''
    st.session_state.df = load_data(file)
    st.session_state.name = file.name


def main():
    st.title(":red[Load Data]")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Creating a session
        if 'df' not in st.session_state:
            create_session(file=uploaded_file)

        # Updating session, if a new file is uploaded
        elif st.session_state.df is not None:
            st.warning(":red[Progress might be lost]")
            if st.button("Load Anyway"):
                create_session(file=uploaded_file)


if __name__ == "__main__":
    main()
