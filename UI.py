import abc
import tkinter as tk
from tkinter import ttk
import matplotlib as plt
import seaborn as sns
from abc import abstractmethod
from data_manager import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
matplotlib.use('TkAgg')
import sv_ttk


class UI:
    def __init__(self, root):
        self.root = root
        sv_ttk.set_theme("dark", root=self.root)
        self.root.title("Food Delivery Data Visualizer")
        self.create_style()
        self.component_init()

    def create_style(self):
        self.label_font = ttk.Style()
        self.label_font.configure('TLabel', font=('Arial',18))

    def component_init(self):
        self.menu_frame = tk.Frame(self.root)
        self.data_tab_button = tk.Button(self.menu_frame, text='Data', command=lambda: self.change_tab('data'))
        self.hist_tab_button = tk.Button(self.menu_frame, text='Histogram', command=lambda: self.change_tab('hist'))
        self.bar_tab_button = tk.Button(self.menu_frame, text='Bar Graph', command=lambda: self.change_tab('bar'))
        self.story_tab_button = tk.Button(self.menu_frame, text='Story', command=lambda: self.change_tab('story'))
        self.quit_button = tk.Button(self.menu_frame, text='Quit', command=self.root.destroy)

        self.data_tab = Data_Tab(self.root)
        self.bar_tab = Bar_Tab(self.root)
        self.hist_tab = Hist_Tab(self.root)

        self.config_grid()
        self.component_install()

        # Defualt tab
        # No matter how much I tried, I cannot make the default button text yellow on launch. I do not know why so, it is what it is.
        self.current_tab = self.bar_tab
        self.change_tab('bar')

    def config_grid(self):
        self.menu_frame.columnconfigure((0,1,2,3,4), weight=1, uniform=True)
        self.menu_frame.rowconfigure(0, weight=1, uniform=True)

    def component_install(self):
        self.data_tab_button.grid(column=0, row=0, sticky=tk.NSEW)
        self.hist_tab_button.grid(column=1, row=0, sticky=tk.NSEW)
        self.bar_tab_button.grid(column=2, row=0, sticky=tk.NSEW)
        self.story_tab_button.grid(column=3, row=0, sticky=tk.NSEW)
        self.quit_button.grid(column=4, row=0, sticky=tk.NSEW)

        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

    def change_tab(self, tab):
        self.reset_menu_color()
        self.current_tab.unpack()
        match tab:
            case 'data':
                self.data_tab_button.config(bg='Yellow', fg='Black')
                self.current_tab = self.data_tab
            case 'hist':
                self.hist_tab_button.config(bg='Yellow', fg='Black')
                self.current_tab = self.hist_tab
            case 'bar':
                self.bar_tab_button.configure(bg='Yellow', fg='Black')
                self.current_tab = self.bar_tab
            case 'story':
                pass
            case _:
                pass
        self.current_tab.pack_tab()

    def reset_menu_color(self):
        self.data_tab_button.config(bg='Black', fg='White')
        self.hist_tab_button.config(bg='Black', fg='White')
        self.bar_tab_button.config(bg='Black', fg='White')
        self.story_tab_button.config(bg='Black', fg='White')
        self.quit_button.config(bg='Black', fg='White')

    @property
    def screenwidth(self):
        return self.root.winfo_screenwidth()

    @property
    def screenheight(self):
        return self.root.winfo_screenheight()

    def run(self):
        self.root.mainloop()


#abstract class for every tabs
class New_Tab(tk.Frame):
    def __init__(self, root):
        self.root = root
        super().__init__(root)
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
        self.table_frame = ttk.Frame(self)
        self.filters_frame = ttk.Frame(self)
        self.table = ttk.Treeview(self.table_frame, columns=self.data.get_cols(), displaycolumns="#all", show="headings")
        self.table_col_config()
        self.set_table_col()
        self.insert_data()
        self.filter_text = ttk.Label(self.filters_frame, text="Filters")
        self.quantity_filter_text = ttk.Label(self.filters_frame, text="Quantity of Items")
        self.quantity_filter_var = tk.StringVar(self.filters_frame, "1-7, 5")
        self.quantity_filter_entry = ttk.Entry(self.filters_frame, textvariable=self.quantity_filter_var)

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


class Hist_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)
        self.grid_config()

    def component_init(self):
        self.graph_frame = ttk.Frame(self)
        self.selection_frame = ttk.Frame(self)

        self.graph_img = FigureCanvasTkAgg(self.data.figure, master=self.graph_frame)
        NavigationToolbar2Tk(self.graph_img, self)

        self.restaurant_button = tk.Button(self.selection_frame, text="Restaurant Name", bg="Black", command=lambda: self.handle_graph('Restaurant Name'))
        self.cuisine_button = tk.Button(self.selection_frame, text="Cuisine", bg="Black", command=lambda: self.handle_graph('Cuisine'))
        self.zone_button = tk.Button(self.selection_frame, text="Zone", bg="Black", command=lambda: self.handle_graph('Zone'))
        self.category_button = tk.Button(self.selection_frame, text="Category", bg="Black", command=lambda: self.handle_graph('Category'))
        self.payment_button = tk.Button(self.selection_frame, text="Payment Mode", bg="Black", command=lambda: self.handle_graph('Payment Mode'))
        self.quantity_button = tk.Button(self.selection_frame, text="Quantity of Items", bg="Black", command=lambda: self.handle_graph('Quantity of Items'))
        self.delivery_button = tk.Button(self.selection_frame, text="Delivery Time", bg="Black", command=lambda: self.handle_graph('Delivery Time'))
        self.food_rate_button = tk.Button(self.selection_frame, text="Food Rating", bg="Black", command=lambda: self.handle_graph('Food Rating'))
        self.deli_rate_button = tk.Button(self.selection_frame, text="Delivery Rating", bg="Black", command=lambda: self.handle_graph('Delivery Rating'))

        self.density_var = tk.BooleanVar()
        self.density_toggle = ttk.Checkbutton(self.selection_frame, variable=self.density_var, text='Density', onvalue=True, offvalue=False, command=lambda: self.handle_graph(-99))

        # Default
        self.handle_graph('Restaurant Name')

    def component_install(self):
        self.graph_img.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.graph_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.restaurant_button.grid(column=0, row=0, sticky=tk.NSEW)
        self.cuisine_button.grid(column=1, row=0, sticky=tk.NSEW)
        self.zone_button.grid(column=2, row=0, sticky=tk.NSEW)
        self.category_button.grid(column=3, row=0, sticky=tk.NSEW)
        self.payment_button.grid(column=4, row=0, sticky=tk.NSEW)
        self.quantity_button.grid(column=5, row=0, sticky=tk.NSEW)
        self.delivery_button.grid(column=6, row=0, sticky=tk.NSEW)
        self.food_rate_button.grid(column=7, row=0, sticky=tk.NSEW)
        self.deli_rate_button.grid(column=8, row=0, sticky=tk.NSEW)
        self.density_toggle.grid(column=9, row=0, sticky=tk.NSEW)
        self.selection_frame.pack(side=tk.TOP, fill=tk.X)

    def grid_config(self):
        self.columnconfigure(0)
        self.columnconfigure(1)

        self.rowconfigure(0, weight=1)

        self.selection_frame.columnconfigure((0,1,2,3,4,5,6,7,8,9), weight=1, uniform=True)
        self.selection_frame.rowconfigure(0, weight=0)


    def handle_graph(self, col):
        if col != -99:
            self.reset_button_color()
        match col:
            case 'Restaurant Name':
                self.restaurant_button.config(bg='Yellow', fg='Black')
            case 'Cuisine':
                self.cuisine_button.config(bg='Yellow', fg='Black')
            case 'Zone':
                self.zone_button.config(bg='Yellow', fg='Black')
            case 'Category':
                self.category_button.config(bg='Yellow', fg='Black')
            case 'Payment Mode':
                self.category_button.config(bg='Yellow', fg='Black')
            case 'Quantity of Items':
                self.quantity_button.config(bg='Yellow', fg='Black')
            case 'Delivery Time':
                self.delivery_button.config(bg='Yellow', fg='Black')
            case 'Food Rating':
                self.food_rate_button.config(bg='Yellow', fg='Black')
            case 'Delivery Rating':
                self.deli_rate_button.config(bg='Yellow', fg='Black')
        self.data.histogram(col, self.density_var.get())
        self.graph_img.draw()

    def reset_button_color(self):
        self.restaurant_button.config(bg='Black', fg='White')
        self.restaurant_button.config(bg='Black', fg='White')
        self.cuisine_button.config(bg='Black', fg='White')
        self.zone_button.config(bg='Black', fg='White')
        self.category_button.config(bg='Black', fg='White')
        self.payment_button.config(bg='Black', fg='White')
        self.quantity_button.config(bg='Black', fg='White')
        self.delivery_button.config(bg='Black', fg='White')
        self.food_rate_button.config(bg='Black', fg='White')
        self.deli_rate_button.config(bg='Black', fg='White')


class Bar_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)
        self.grid_config()

    def component_init(self):
        self.graph_frame = ttk.Frame(self)
        self.config_frame = ttk.Frame(self)

        self.graph_img = FigureCanvasTkAgg(self.data.figure, master=self.graph_frame)
        NavigationToolbar2Tk(self.graph_img, self)

        self.config_text = ttk.Label(self.config_frame, text="Config")

        self.bar_config_text = ttk.Label(self.config_frame, text="Bar")
        self.bar_config_combobox = ttk.Combobox(self.config_frame, values=self.data.get_nominal_cols(), state='readonly')
        self.bar_config_combobox.current(0)
        self.bar_config_combobox.bind('<<ComboboxSelected>>', self.handle_graph)

        self.height_config_text = ttk.Label(self.config_frame, text="Height")
        self.height_config_combobox = ttk.Combobox(self.config_frame, values=self.data.get_numerical_cols(), state='readonly')
        self.height_config_combobox.current(0)
        self.height_config_combobox.bind('<<ComboboxSelected>>', self.handle_graph)

        self.values_config_text = ttk.Label(self.config_frame, text="Values")
        self.values_config_combobox = ttk.Combobox(self.config_frame, values=['AVERAGE', 'SUM'], state='readonly')
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
        self.config_frame.pack(padx=10, side=tk.RIGHT, fill=tk.BOTH)

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
        self.data.bar_graph(self.bar_config_combobox.get(), self.height_config_combobox.get(), self.values_config_combobox.get())
        self.graph_img.draw()



if __name__ == '__main__':
    root = tk.Tk()
    ui = UI(root)
    ui.run()