import pandas as pd
import streamlit as st


class EncodeData():
    def __init__(self, df) -> None:
        self.df = df

    def handle_missing_data(self):
        try:
            if self.df is not None:
                st.write(self.df.size)
                st.markdown(f":red[red]")
            else:
                st.markdown(f":blue[blue!]")
        except: st.markdown(f":red[hey!]")
