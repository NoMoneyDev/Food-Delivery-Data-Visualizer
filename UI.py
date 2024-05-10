import abc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib as plt
import seaborn as sns
from abc import abstractmethod
from data_manager import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
matplotlib.use('TkAgg')
import sv_ttk
import time
import os
from PIL import Image, ImageTk


class UI:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
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
        self.descriptive_tab_button = tk.Button(self.menu_frame, text='Descriptive', command=lambda: self.change_tab('desc'))
        self.quit_button = tk.Button(self.menu_frame, text='Quit', command=self.root.destroy)

        self.data_tab = Data_Tab(self.root)
        self.bar_tab = Bar_Tab(self.root)
        self.hist_tab = Hist_Tab(self.root)
        self.story_tab = Story_Tab(self.root)
        self.descriptive_tab = Descriptive_Tab(self.root)
        self.config_grid()
        self.component_install()

        # Defualt tab
        # No matter how much I tried, I cannot make the default button text yellow on launch. I do not know why, so it is what it is.
        self.current_tab = self.bar_tab
        self.change_tab('data')

    def config_grid(self):
        self.menu_frame.columnconfigure((0,1,2,3,4,5), weight=1, uniform=True)
        self.menu_frame.rowconfigure(0, weight=1, uniform=True, minsize=30)

    def component_install(self):
        self.data_tab_button.grid(column=0, row=0, sticky=tk.NSEW)
        self.hist_tab_button.grid(column=1, row=0, sticky=tk.NSEW)
        self.bar_tab_button.grid(column=2, row=0, sticky=tk.NSEW)
        self.story_tab_button.grid(column=3, row=0, sticky=tk.NSEW)
        self.descriptive_tab_button.grid(column=4, row=0, sticky=tk.NSEW)
        self.quit_button.grid(column=5, row=0, sticky=tk.NSEW)

        self.menu_frame.pack(side=tk.TOP, fill=tk.BOTH)

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
                self.story_tab_button.configure(bg='Yellow', fg='Black')
                self.current_tab = self.story_tab
            case 'desc':
                self.descriptive_tab_button.configure(bg='Yellow', fg='Black')
                self.current_tab = self.descriptive_tab
        self.current_tab.pack_tab()

    def reset_menu_color(self):
        self.data_tab_button.config(bg='Black', fg='White')
        self.hist_tab_button.config(bg='Black', fg='White')
        self.bar_tab_button.config(bg='Black', fg='White')
        self.story_tab_button.config(bg='Black', fg='White')
        self.descriptive_tab_button.config(bg='Black', fg='White')
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
        self.font = ('Arial', 12)
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
        scrnwidth = self.root.winfo_screenwidth()
        self.table_frame = ttk.Frame(self, width=scrnwidth*0.55)
        self.filters_frame = ttk.Frame(self)
        self.table = ttk.Treeview(self.table_frame, columns=self.data.get_cols(), displaycolumns="#all", show="headings")
        self.table_col_config()
        self.set_table_col()
        self.insert_data()
        self.filter_text = ttk.Label(self.filters_frame, text="Filters")

        self.quantity_frame = tk.Frame(self.filters_frame)
        self.quantity_filter_text = tk.Label(self.quantity_frame, text="Quantity of Items", font=self.font)
        self.quantity_filter_var = tk.StringVar(self.quantity_frame, "1-7, 5")
        self.quantity_filter_entry = ttk.Entry(self.quantity_frame, textvariable=self.quantity_filter_var)
        self.quantity_filter_entry.bind('<Return>', lambda ev: self.handle_filter(ev, 'Quantity of Items', self.quantity_filter_var.get()))

        self.cost_frame = tk.Frame(self.filters_frame)
        self.cost_filter_text = tk.Label(self.cost_frame, text="Cost", font=self.font)
        self.cost_filter_var = tk.StringVar(self.cost_frame, "100-700")
        self.cost_filter_entry = ttk.Entry(self.cost_frame, textvariable=self.cost_filter_var)
        self.cost_filter_entry.bind('<Return>', lambda ev: self.handle_filter(ev, 'Cost', self.cost_filter_var.get()))

        self.payment_frame = tk.Frame(self.filters_frame)
        self.payment_filter_text = tk.Label(self.payment_frame, text="Payment mode", font=self.font)
        self.payment_filter_listbox = tk.Listbox(self.payment_frame, selectmode=tk.MULTIPLE, height=3, selectbackground='grey', relief=tk.FLAT, highlightcolor='black')
        self.payment_filter_listbox.insert(tk.END, 'Cash','Credit Card','Debit Card')
        self.payment_filter_listbox.bind('<Button-1>', lambda ev: self.check_deselect())

        self.food_rate_frame = tk.Frame(self.filters_frame)
        self.food_rate_filter_text = tk.Label(self.food_rate_frame, text="Food Rating", font=self.font)
        self.food_rate_filter_var = tk.StringVar(self.food_rate_frame, "1-3, 5")
        self.food_rate_filter_entry = ttk.Entry(self.food_rate_frame, textvariable=self.food_rate_filter_var)
        self.food_rate_filter_entry.bind('<Return>', lambda ev: self.handle_filter(ev, 'Food Rating', self.food_rate_filter_var.get()))

        self.deli_rate_frame = tk.Frame(self.filters_frame)
        self.deli_rate_filter_text = tk.Label(self.deli_rate_frame, text="Delivery Rating", font=self.font)
        self.deli_rate_filter_var = tk.StringVar(self.deli_rate_frame, "1-3, 5")
        self.deli_rate_filter_entry = ttk.Entry(self.deli_rate_frame, textvariable=self.deli_rate_filter_var)
        self.deli_rate_filter_entry.bind('<Return>', lambda ev: self.handle_filter(ev, 'Delivery Rating', self.deli_rate_filter_var.get()))

        self.active_filter = {}
        for col in self.data.get_cols():
            self.active_filter[col] = ''

    def component_install(self):
        self.table.pack(side=tk.LEFT, fill=tk.Y)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.filter_text.grid(column=1, row=0, sticky=tk.W)

        self.quantity_frame.grid(column=1, row=1)
        self.quantity_filter_text.pack()
        self.quantity_filter_entry.pack()

        self.cost_frame.grid(column=2, row=1)
        self.cost_filter_text.pack()
        self.cost_filter_entry.pack()

        self.payment_frame.grid(column=3, row=1)
        self.payment_filter_text.pack()
        self.payment_filter_listbox.pack()

        self.food_rate_frame.grid(column=1, row=2)
        self.food_rate_filter_text.pack()
        self.food_rate_filter_entry.pack()

        self.deli_rate_frame.grid(column=2, row=2)
        self.deli_rate_filter_text.pack()
        self.deli_rate_filter_entry.pack()

        self.filters_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


    def table_col_config(self):
        for i,col in enumerate(self.data.get_cols()):
            self.table.heading('#'+str(i), text=col)

        self.table.column('#0', minwidth=0, stretch=True)

        optimal_width = int(self.root.winfo_screenwidth()/18)

        for col_num in range(2,len(self.data.get_cols())):
            self.table.column('#'+str(col_num), minwidth=0, width=optimal_width, stretch=False)



    def grid_config(self):
        self.filters_frame.columnconfigure(0, weight=1, uniform=True)
        self.filters_frame.columnconfigure(1, weight=1, uniform=True)
        self.filters_frame.columnconfigure(2, weight=1, uniform=True)
        self.filters_frame.columnconfigure(3, weight=1, uniform=True)
        self.filters_frame.columnconfigure(4, weight=1, uniform=True)

        self.filters_frame.rowconfigure(0, weight=1)
        self.filters_frame.rowconfigure(1, weight=1)
        self.filters_frame.rowconfigure(2, weight=1)
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

    def clear_data(self):
        self.table.delete(*self.table.get_children())

    def reset_filter(self, event):
        label = self.get_filter_label(event)
        label.config(fg='white')

        match label:
            case self.quantity_filter_text:
                self.quantity_filter_var.set('1-7, 5')

            case self.cost_filter_text:
                self.cost_filter_var.set('100-700')

            case self.food_rate_filter_text:
                self.food_rate_filter_var.set('1-3, 5')

            case self.deli_rate_filter_text:
                self.deli_rate_filter_var.set('1-3, 5')

    def check_deselect(self):
        self.root.after(5, self.handle_payment)

    def handle_payment(self):
        filter = []
        listbox = self.payment_filter_listbox
        for i in listbox.curselection():
            filter.append(listbox.get(i))
        match len(filter):
            case 3:
                self.active_filter['Payment Mode'] = [','.join(filter), 'multexact']
            case 2:
                self.active_filter['Payment Mode'] = [','.join(filter), 'multexact']
            case 1:
                self.active_filter['Payment Mode'] = [filter[0], 'exact']
            case 0:
                self.active_filter['Payment Mode'] = ['Cash,Credit Card,Debit Card', 'multexact']
                self.payment_filter_text.config(fg='white')
                self.refresh_data()
                return

        self.payment_filter_text.config(fg='yellow')
        self.refresh_data()

    def handle_filter(self, event, col, filter):
        if filter == '':
            self.reset_filter(event)
            self.active_filter[col] = ''
            self.refresh_data()
            return

        # Check nominal value filter
        if col in self.data.get_nominal_cols():
            if ',' in filter:
                filters = filter.split(',')
                valid_cols = self.data[col].unique()
                if not all(c in valid_cols for c in filters):
                    messagebox.showerror('INVALID FILTER VALUES', 'Value Error: All values in the filter must be in the data')
                    return
                mode = 'multexact'
            else:
                if filter not in self.data[col].unique():
                    messagebox.showerror('INVALID FILTER VALUE', 'Value Error: Filter value must be in the data')
                    return
                mode = 'exact'

        # Check numerical value filter (must be integer)
        elif col in self.data.get_numerical_cols():
            if '-' in filter:
                filters = filter.split('-')
                if not all(c.isdigit() for c in filters):
                    messagebox.showerror('INVALID FILTER VALUES', 'Type Error: Filter value must be integer')
                    return
                mode = 'range'
            else:
                if not filter.isdigit():
                    messagebox.showerror('INVALID FILTER VALUES', 'Type Error: Filter value must be integer')
                    return
                filters = filter
                mode = 'exact'

        self.get_filter_label(event).config(fg='Yellow')
        self.active_filter[col] = [filter, mode]
        self.refresh_data()

    def get_filter_label(self, event):
        return event.widget.master.winfo_children()[0]

    def refresh_data(self):
        new_data = self.data.filter_data(self.active_filter)
        self.clear_data()

        for row in new_data:
            self.table.insert('', tk.END, values=row)


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


class Story_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)

    def component_init(self):
        self.graph_frame = tk.Frame(self)
        path = os.getcwd()
        img_name = 'Scatter plot of Quantity of items and Cost.png'
        img_path = os.path.join(path, 'img')
        img = os.path.abspath(os.path.join(img_path,img_name))
        img = 'img/Scatter plot of Quantity of items and Cost.png'

        self.graph_img = tk.PhotoImage(master=self.graph_frame, file=img)

        self.correl_frame = tk.Frame(self)
        self.correl_img = tk.Label(self.graph_frame, image=img)

        self.desc_frame = tk.Frame(self)
        self.description = tk.Label(self.desc_frame, text='', fg='white')

    def component_install(self):
        self.graph_img.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.correl_img.pack(fill=tk.BOTH, expand=True)
        self.correl_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.description.pack(fill=tk.BOTH)
        self.desc_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class Descriptive_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)

    def component_init(self):
        pass

    def component_install(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    ui = UI(root)
    ui.run()