import abc
import tkinter as tk
from tkinter import ttk
import matplotlib as plt
import seaborn as sns
from abc import abstractmethod
from data_manager import *


class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Delivery Data Visualizer")

        self.component_init()


    def component_init(self):
        self.menubar = tk.Menu(self.root)

        self.menubar.add_cascade(label="Data", command=lambda: self.change_tab('data'))
        self.menubar.add_cascade(label="Histogram", command=lambda: self.change_tab('hist'))
        self.menubar.add_cascade(label="Bar Graph", command=lambda: self.change_tab('bar'))
        self.menubar.add_cascade(label="Data Story", command=lambda: self.change_tab('story'))

        self.data_tab = Data_Tab(self.root)

        self.component_install()
        self.change_tab('data')

    def component_install(self):
        self.root.config(menu=self.menubar)

    def change_tab(self, tab):
        match tab:
            case 'data':
                print("Changed Tab to 'Data'")
                self.data_tab.pack_tab()
            case _:
                pass

    def run(self):
        self.root.mainloop()


class New_Tab(tk.Frame):
    def __init__(self, root):
        self.root = root
        super().__init__()
        self.components = []
        self.component_init()

    @abstractmethod
    def component_init(self):
        pass

    def pack_tab(self):
        for ele in self.components:
            ele.pack()


class Data_Tab(New_Tab):
    def __init__(self, root):
        self.data = Data_Manager()
        super().__init__(root)

    def component_init(self):
        self.components = [self]
        self.table = ttk.Treeview(self, columns=self.data.get_cols(), displaycolumns="#all", show="headings")
        self.set_table_col()
        self.table.insert('',tk.END, values=('Anand Restaurant','African','Zone C','Ordinary','Credit Card',1,80,39,5,1))

        self.components += [self.table]

    def set_table_col(self):
        cols = self.data.get_cols()
        for c in cols:
            self.table.heading(c, text=c)


