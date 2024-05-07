import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np


class Data_Manager:
    def __init__(self):
        self.__data = pd.read_csv("Orders Data.csv")
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot()

    def get_cols(self):
        return  self.data.columns.tolist()

    def get_nominal_cols(self):
        return ['Restaurant Name','Cuisine','Zone','Category','Payment Mode']

    def get_numerical_cols(self):
        return ['Quantity of Items','Cost','Delivery Time','Food Rating','Delivery Rating']

    @property
    def data(self):
        return self.__data

    def get_rows(self):
        returnlist = []
        for row in self.data.itertuples():
            returnlist += [list(row)[1:]]
        return returnlist

    def histogram(self, col):
        self.ax.clear()
        if col in self.get_nominal_cols():
            cols = self.data[col].unique().tolist()
            counts = []
            for c in cols:
                counts += [self.data[col].value_counts()[c]]
            self.ax.bar(x=cols, height=counts)
        else:
            cols = self.data[col].unique().tolist()
            self.ax.hist(self.data[col].tolist(), edgecolor="white", rwidth=1, align='left', bins=range(min(cols),max(cols)))
        self.ax.set_xlabel(col)
        self.ax.set_ylabel('Frequency')

    def bar_graph(self, bar, height, val):
        h_val = []
        self.ax.clear()
        df = self.data
        cols = df[bar].unique().tolist()
        match val:
            case 'SUM':
                for col in cols:
                    h_val += [df[df[bar] == col][height].sum()]
                self.ax.bar(x=cols, height=h_val)
                self.ax.set_title(f"Sum of {height} to {bar}")
            case 'AVERAGE':
                for col in cols:
                    h_val += [df[df[bar] == col][height].mean()]
                self.ax.bar(x=cols, height=h_val)
                self.ax.set_title(f"Average {height} to {bar}")
        self.ax.set_xlabel(bar)
        self.ax.set_ylabel(height)

