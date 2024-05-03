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

    @abstractmethod
    def component_init(self):
        pass

    @abstractmethod
    def pack_tab(self):
        pass


class Data_Tab(New_Tab):
    def __init__(self, root):
        self.data = Data_Manager()
        super().__init__(root)
        self.component_init()
        self.grid_config()

    def component_init(self):
        self.table_frame = tk.Frame(self)
        self.filters_frame = tk.Frame(self)
        self.table = ttk.Treeview(self.table_frame, columns=self.data.get_cols(), displaycolumns="#all", show="headings")
        self.table_col_config()
        self.set_table_col()
        self.insert_data()
        self.filter_text = tk.Label(self.filters_frame, text="Filters", font=('Arial', 14))
        self.quantity_filter_text = tk.Label(self.filters_frame, text="Quantity of Items")
        self.quantity_filter_var = tk.StringVar(self.filters_frame, "1-7, 5")
        self.quantity_filter_var
        self.quantity_filter_entry = tk.Entry(self.filters_frame, textvariable=self.quantity_filter_var)

    def pack_tab(self):
        self.table.pack(fill=tk.BOTH, expand=True)
        self.table_frame.grid(column=0, row=0, sticky=tk.NSEW)

        self.filter_text.grid(column=0, row=0, sticky=tk.W)
        self.quantity_filter_text.grid(column=0, row=1, sticky=tk.SW)
        self.quantity_filter_entry.grid(column=0, row=2, sticky=tk.NW)
        self.filters_frame.grid(column=1, row=0, sticky=tk.NSEW)

        self.pack(fill=tk.Y, expand=True)

    def table_col_config(self):
        for col_num in range(len(self.data.get_cols())):
            self.table.column('#'+str(col_num+1), minwidth = 70, width=155,  stretch=True)

    def grid_config(self):
        self.columnconfigure(0, weight=3, uniform=True)
        self.columnconfigure(1, weight=2, uniform=True)

        self.rowconfigure(0,weight=1)

        self.filters_frame.columnconfigure(0, weight=1, uniform=True)
        self.filters_frame.columnconfigure(1, weight=1, uniform=True)
        self.filters_frame.columnconfigure(2, weight=1, uniform=True)

        self.filters_frame.rowconfigure(0, weight=1, uniform=True)
        self.filters_frame.rowconfigure(1, weight=1, uniform=True)
        self.filters_frame.rowconfigure(2, weight=1, uniform=True)
        self.filters_frame.rowconfigure(3, weight=1, uniform=True)
        self.filters_frame.rowconfigure(4, weight=1, uniform=True)
        self.filters_frame.rowconfigure(5, weight=1, uniform=True)
        self.filters_frame.rowconfigure(6, weight=1, uniform=True)
        self.filters_frame.rowconfigure(7, weight=1, uniform=True)
        self.filters_frame.rowconfigure(8, weight=1, uniform=True)
        self.filters_frame.rowconfigure(9, weight=1, uniform=True)

    def set_table_col(self):
        cols = self.data.get_cols()
        for c in cols:
            self.table.heading(c, text=c)

    def insert_data(self):
        for row in self.data.get_rows():
            self.table.insert('', tk.END, values=row)



if __name__ == '__main__':
    root = tk.Tk()
    ui = UI(root)
    ui.run()