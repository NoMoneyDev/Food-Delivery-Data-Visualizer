import abc
import tkinter as tk
from tkinter import ttk
import matplotlib as plt
import seaborn as sns
from abc import abstractmethod
from data_manager import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
matplotlib.use('TkAgg')


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
        self.menubar.add_cascade(label="Quit", command=self.root.destroy)

        self.data_tab = Data_Tab(self.root)
        self.bar_tab = Bar_Tab(self.root)

        self.component_install()

        # Defualt tab
        self.current_tab = self.data_tab
        self.change_tab('data')

    def component_install(self):
        self.root.config(menu=self.menubar)

    def change_tab(self, tab):
        self.current_tab.unpack()
        match tab:
            case 'data':
                self.current_tab = self.data_tab
            case 'hist':
                pass
            case 'bar':
                self.current_tab = self.bar_tab
            case _:
                pass
        self.current_tab.pack_tab()

    @property
    def screenwidth(self):
        return self.root.winfo_screenwidth()

    @property
    def screenheight(self):
        return self.root.winfo_screenheight()

    def run(self):
        self.root.mainloop()


class New_Tab(tk.Frame):
    def __init__(self, root):
        self.root = root
        super().__init__()
        self.data = Data_Manager()
        self.component_init()
        self.component_install()

    @abstractmethod
    def component_init(self):
        pass

    @abstractmethod
    def pack_tab(self):
        self.pack(fill=tk.BOTH, expand=True)

    @abstractmethod
    def unpack(self):
        self.pack_forget()


class Data_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)
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

    def component_install(self):
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.table_frame.grid(column=0, row=0, sticky=tk.NSEW)

        self.filter_text.grid(column=0, row=0, sticky=tk.W)
        self.quantity_filter_text.grid(column=0, row=1, sticky=tk.SW)
        self.quantity_filter_entry.grid(column=0, row=2, sticky=tk.NW)
        self.filters_frame.grid(padx=10, column=1, row=0, sticky=tk.NSEW)

    def table_col_config(self):
        for col_num in range(len(self.data.get_cols())):
            self.table.column('#'+str(col_num+1), minwidth = 65, width=150,  stretch=True)

    def grid_config(self):
        self.columnconfigure(0)
        self.columnconfigure(1)

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

    def unpack(self):
        self.pack_forget()


class Bar_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)
        self.grid_config()

    def component_init(self):
        self.graph_frame = tk.Frame(self)
        self.config_frame = tk.Frame(self)

        self.graph_img = FigureCanvasTkAgg(self.data.figure, master=self.graph_frame)
        NavigationToolbar2Tk(self.graph_img, self)

        self.config_text = tk.Label(self.config_frame, text="Config", font=('Arial', 14))

        self.bar_config_text = tk.Label(self.config_frame, text="Bar")
        self.bar_config_var = tk.StringVar()
        self.bar_config_combobox = ttk.Combobox(self.config_frame, values=self.data.get_cols(),
                                                textvariable=self.bar_config_var, state='readonly')
        self.bar_config_combobox.current(0)
        self.bar_config_combobox.bind('<<ComboboxSelected>>', self.handle_graph)

        self.height_config_text = tk.Label(self.config_frame, text="Height")
        self.height_config_var = tk.StringVar()
        self.height_config_combobox = ttk.Combobox(self.config_frame, values=self.data.get_ordinal_cols(),
                                                   textvariable=self.height_config_var, state='readonly')
        self.height_config_combobox.current(1)
        self.height_config_combobox.bind('<<ComboboxSelected>>', self.handle_graph)

        self.values_config_text = tk.Label(self.config_frame, text="Values")
        self.values_config_var = tk.StringVar()
        self.values_config_combobox = ttk.Combobox(self.config_frame, values=['AVERAGE', 'SUM'],
                                                   textvariable=self.values_config_var, state='readonly')
        self.values_config_combobox.current(0)
        self.values_config_combobox.bind('<<ComboboxSelected>>', self.handle_graph)

        self.handle_graph()

    def component_install(self):
        self.graph_img.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.config_text.grid(column=0, row=0, sticky=tk.W)
        self.bar_config_text.grid(column=0, row=1, sticky=tk.SW, padx=5)
        self.bar_config_combobox.grid(column=0, row=2, sticky=tk.NW, padx=5)
        self.height_config_text.grid(column=1, row=1, sticky=tk.SW, padx=5)
        self.height_config_combobox.grid(column=1, row=2, sticky=tk.NW, padx=5)
        self.values_config_text.grid(column=2, row=1, sticky=tk.SW, padx=5)
        self.values_config_combobox.grid(column=2, row=2, sticky=tk.NW, padx=5)
        self.config_frame.pack(padx=10, side=tk.RIGHT)

    def grid_config(self):
        self.columnconfigure(0)
        self.columnconfigure(1)

        self.rowconfigure(0, weight=1)

        self.config_frame.columnconfigure(0, weight=1, uniform=True)
        self.config_frame.columnconfigure(1, weight=1, uniform=True)
        self.config_frame.columnconfigure(2, weight=1, uniform=True)

        self.config_frame.rowconfigure(0, weight=1, uniform=True)
        self.config_frame.rowconfigure(1, weight=1, uniform=True)
        self.config_frame.rowconfigure(2, weight=1, uniform=True)
        self.config_frame.rowconfigure(3, weight=1, uniform=True)
        self.config_frame.rowconfigure(4, weight=1, uniform=True)
        self.config_frame.rowconfigure(5, weight=1, uniform=True)
        self.config_frame.rowconfigure(6, weight=1, uniform=True)
        self.config_frame.rowconfigure(7, weight=1, uniform=True)
        self.config_frame.rowconfigure(8, weight=1, uniform=True)
        self.config_frame.rowconfigure(9, weight=1, uniform=True)

    def handle_graph(self, *args):
        self.data.bar_graph(self.bar_config_var.get(), self.height_config_var.get(), self.values_config_var.get())
        self.graph_img.draw()



if __name__ == '__main__':
    root = tk.Tk()
    ui = UI(root)
    ui.run()