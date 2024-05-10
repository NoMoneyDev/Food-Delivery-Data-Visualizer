import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np


class Data_Manager:
    def __init__(self):
        self.__data = pd.read_csv("Orders Data.csv")
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.figure.patch.set_facecolor('grey')
        self.ax = self.figure.add_subplot()
        self.__active_hist = ''

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

    def to_row(self, data):
        returnlist = []
        for row in data.itertuples():
            returnlist += [list(row)[1:]]
        return returnlist

    def clear_data(self):
        self.__data = pd.DataFrame(columns=self.data.columns)

    def filter_data(self, filters):
        df = self.data.copy()
        for col,fil in filters.items():
            filter = fil[0]
            mode = fil[1]
            match mode:
                case 'exact':
                    pass
                case 'multexact':
                    pass
                case 'range':
                    df = df[(filter1 <= self.data[col]) & (self.data[col] <= filter2)]

        return self.to_row(df)


    def histogram(self, col, density):
        self.ax.clear()
        self.ax.patch.set_facecolor('black')
        if col == -99:
            col = self.__active_hist
        if col in self.get_nominal_cols():
            cols = self.data[col].unique().tolist()
            counts = []
            if density:
                for c in cols:
                    counts += [self.data[col].value_counts()[c]/self.data[col].count()]
            else:
                for c in cols:
                    counts += [self.data[col].value_counts()[c]]
            self.ax.bar(x=cols, height=counts)
        elif col in ['Quantity of Items']:
            self.ax.hist(self.data[col].tolist(), edgecolor="white", align='left', bins=[1,2,3,4,5,6,7], width=1, density=density)
        elif col in ['Food Rating', 'Delivery Rating']:
            self.ax.hist(self.data[col].tolist(), edgecolor="white", align='mid', bins=[1,2,3,4,5], width=1, density=density)
        else:
            cols = self.data[col].unique().tolist()
            self.ax.hist(self.data[col].tolist(), edgecolor="white", align='mid', bins=range(min(cols),max(cols),5), density=density)
        self.ax.set_title(f"Histogram of {col}")
        self.ax.set_xlabel(col)
        self.ax.set_ylabel('Frequency')
        self.__active_hist = col

    def bar_graph(self, bar, height, val):
        h_val = []
        self.ax.clear()
        self.ax.patch.set_facecolor('black')
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

