import pandas as pd
import numpy as np


class Data_Manager:
    def __init__(self):
        self.__data = pd.read_csv("Orders Data.csv")

    def get_cols(self):
        return list(self.data.columns)

    @property
    def data(self):
        return self.__data

    def get_rows(self):
        returnlist = []
        for row in self.data.itertuples():
            returnlist += [list(row)[1:]]
        return returnlist