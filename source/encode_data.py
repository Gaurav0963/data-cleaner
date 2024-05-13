import pandas as pd
import streamlit as st
from logger import logging as log
from exception import CustomException
from feature_engine.encoding import OneHotEncoder


class EncodeData:
    log.info('In class EncodeData')
    def __init__(self, X_train: pd.DataFrame, X_test=None) -> None:
        self.X_train = X_train
        self.X_test: pd.DataFrame|None = None

    def handle_missing_data(self):...

    def OHE(self) -> pd.DataFrame:
        log.info("Inside OHE")
        try:
            ohe = OneHotEncoder(drop_last=True)
            X_train_enc = ohe.fit_transform(self.X_train)
            X_test_enc = ohe.transform(self.X_test)
            return X_train_enc, X_test_enc
        except CustomException as ce:
            log.warning(f"{ce}")
    
