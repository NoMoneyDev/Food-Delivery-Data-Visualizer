import os
import webbrowser
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from abc import abstractmethod
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sv_ttk
from data_manager import Data_Manager


class UI:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
        sv_ttk.set_theme("dark", root=self.root)
        self.root.title("Food Delivery Data Visualizer")
        path = os.path.join(os.getcwd(), 'img', 'logo.png')
        icon = Image.open(path)
        logo = ImageTk.PhotoImage(icon)
        root.wm_iconphoto(False, logo)
        self.create_style()
        self.component_init()

    def create_style(self):
        self.label_font = ttk.Style()
        self.label_font.configure('TLabel', font=('Arial', 18))

    def component_init(self):
        self.menu_frame = tk.Frame(self.root)
        self.data_tab_button = tk.Button(self.menu_frame, text='Data',
                                         command=lambda: self.change_tab('data'))
        self.hist_tab_button = tk.Button(self.menu_frame, text='Histogram',
                                         command=lambda: self.change_tab('hist'))
        self.bar_tab_button = tk.Button(self.menu_frame, text='Bar Graph',
                                        command=lambda: self.change_tab('bar'))
        self.story_tab_button = tk.Button(self.menu_frame, text='Story',
                                          command=lambda: self.change_tab('story'))
        self.descriptive_tab_button = tk.Button(self.menu_frame, text='Descriptive',
                                                command=lambda: self.change_tab('desc'))
        self.about_tab_button = tk.Button(self.menu_frame, text='About',
                                          command=lambda: self.change_tab('about'))
        self.quit_button = tk.Button(self.menu_frame, text='Quit', command=self.root.destroy)

        self.data_tab = Data_Tab(self.root)
        self.bar_tab = Bar_Tab(self.root)
        self.hist_tab = Hist_Tab(self.root)
        self.story_tab = Story_Tab(self.root)
        self.descriptive_tab = Descriptive_Tab(self.root)
        self.about_tab = About_Tab(self.root)
        self.config_grid()
        self.component_install()

        # Defualt tab
        # No matter how much I tried, I cannot make the default button text yellow on launch.
        # I do not know why, so it is what it is.
        self.current_tab = self.bar_tab
        self.change_tab('data')

    def config_grid(self):
        self.menu_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform=True)
        self.menu_frame.rowconfigure(0, weight=1, uniform=True, minsize=self.screenheight // 48)

    def component_install(self):
        self.data_tab_button.grid(column=0, row=0, sticky=tk.NSEW)
        self.hist_tab_button.grid(column=1, row=0, sticky=tk.NSEW)
        self.bar_tab_button.grid(column=2, row=0, sticky=tk.NSEW)
        self.story_tab_button.grid(column=3, row=0, sticky=tk.NSEW)
        self.descriptive_tab_button.grid(column=4, row=0, sticky=tk.NSEW)
        self.about_tab_button.grid(column=5, row=0, sticky=tk.NSEW)
        self.quit_button.grid(column=6, row=0, sticky=tk.NSEW)

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
            case 'about':
                self.about_tab_button.configure(bg='Yellow', fg='Black')
                self.current_tab = self.about_tab
        self.current_tab.pack_tab()

    def reset_menu_color(self):
        self.data_tab_button.config(bg='Black', fg='White')
        self.hist_tab_button.config(bg='Black', fg='White')
        self.bar_tab_button.config(bg='Black', fg='White')
        self.story_tab_button.config(bg='Black', fg='White')
        self.descriptive_tab_button.config(bg='Black', fg='White')
        self.about_tab_button.config(bg='Black', fg='White')
        self.quit_button.config(bg='Black', fg='White')

    @property
    def screenwidth(self):
        return self.root.winfo_screenwidth()

    @property
    def screenheight(self):
        return self.root.winfo_screenheight()

    def run(self):
        self.root.mainloop()


# abstract class for every tabs
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

    def pack_tab(self):
        self.pack(fill=tk.BOTH, expand=True)

    def unpack(self):
        self.pack_forget()


class Data_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)
        self.grid_config()

    def component_init(self):
        scrnwidth = self.root.winfo_screenwidth()
        self.table_frame = ttk.Frame(self, width=scrnwidth * 0.55)
        self.filters_frame = ttk.Frame(self)
        self.table = ttk.Treeview(self.table_frame, columns=self.data.get_cols(),
                                  displaycolumns="#all", show="headings")
        self.table_col_config()
        self.set_table_col()
        self.insert_data()
        self.filter_text = ttk.Label(self.filters_frame, text="Filters")

        self.quantity_frame = tk.Frame(self.filters_frame)
        self.quantity_filter_text = tk.Label(self.quantity_frame, text="Quantity of Items",
                                             font=self.font)
        self.quantity_filter_var = tk.StringVar(self.quantity_frame, "1-7, 5")
        self.quantity_filter_entry = ttk.Entry(self.quantity_frame,
                                               textvariable=self.quantity_filter_var)
        self.quantity_filter_entry.bind('<Return>',
                                        lambda ev: self.handle_filter(ev, 'Quantity of Items',
                                                                  self.quantity_filter_var.get()))

        self.cost_frame = tk.Frame(self.filters_frame)
        self.cost_filter_text = tk.Label(self.cost_frame, text="Cost", font=self.font)
        self.cost_filter_var = tk.StringVar(self.cost_frame, "100-700")
        self.cost_filter_entry = ttk.Entry(self.cost_frame, textvariable=self.cost_filter_var)
        self.cost_filter_entry.bind('<Return>',
                                    lambda ev: self.handle_filter(ev, 'Cost',
                                                                self.cost_filter_var.get()))

        self.payment_frame = tk.Frame(self.filters_frame)
        self.payment_filter_text = tk.Label(self.payment_frame,
                                            text="Payment mode",
                                            font=self.font)
        self.payment_filter_listbox = tk.Listbox(self.payment_frame,
                                                 selectmode=tk.MULTIPLE, height=3,
                                                 selectbackground='grey', relief=tk.FLAT,
                                                 highlightcolor='black',
                                                 exportselection=False)
        self.payment_filter_listbox.insert(tk.END, 'Cash', 'Credit Card', 'Debit Card')
        self.payment_filter_listbox.bind('<Button-1>', lambda ev: self.check_deselect(ev))

        self.food_rate_frame = tk.Frame(self.filters_frame)
        self.food_rate_filter_text = tk.Label(self.food_rate_frame, text="Food Rating", font=self.font)
        self.food_rate_filter_var = tk.StringVar(self.food_rate_frame, "1-3, 5")
        self.food_rate_filter_entry = ttk.Entry(self.food_rate_frame, textvariable=self.food_rate_filter_var)
        self.food_rate_filter_entry.bind('<Return>', lambda ev: self.handle_filter(ev, 'Food Rating',
                                                                                   self.food_rate_filter_var.get()))

        self.deli_rate_frame = tk.Frame(self.filters_frame)
        self.deli_rate_filter_text = tk.Label(self.deli_rate_frame, text="Delivery Rating", font=self.font)
        self.deli_rate_filter_var = tk.StringVar(self.deli_rate_frame, "1-3, 5")
        self.deli_rate_filter_entry = ttk.Entry(self.deli_rate_frame, textvariable=self.deli_rate_filter_var)
        self.deli_rate_filter_entry.bind('<Return>', lambda ev: self.handle_filter(ev, 'Delivery Rating',
                                                                                   self.deli_rate_filter_var.get()))

        self.zone_frame = tk.Frame(self.filters_frame)
        self.zone_filter_text = tk.Label(self.zone_frame, text="Zone", font=self.font)
        self.zone_filter_listbox = tk.Listbox(self.zone_frame, selectmode=tk.MULTIPLE, height=4,
                                              selectbackground='grey', relief=tk.FLAT, highlightcolor='black',
                                              exportselection=False)
        self.zone_filter_listbox.insert(tk.END, 'Zone A', 'Zone B', 'Zone C', 'Zone D')
        self.zone_filter_listbox.bind('<Button-1>', lambda ev: self.check_deselect(ev))

        self.restaurant_frame = tk.Frame(self.filters_frame)
        self.restaurant_filter_text = tk.Label(self.restaurant_frame, text="Restaurant Name", font=self.font)
        self.restaurant_filter_var = tk.StringVar()
        self.restaurant_filter_combobox = ttk.Combobox(self.restaurant_frame,
                                                       values=['None'] + self.data.get_unique_val('Restaurant Name'),
                                                       textvariable=self.restaurant_filter_var, state='readonly')
        self.restaurant_filter_combobox.current(0)
        self.restaurant_filter_combobox.bind('<<ComboboxSelected>>',
                                             lambda ev: self.handle_filter(ev, 'Restaurant Name',
                                                                self.restaurant_filter_var.get()))

        self.category_frame = tk.Frame(self.filters_frame)
        self.category_filter_text = tk.Label(self.category_frame, text="Category", font=self.font)
        self.category_filter_var = tk.StringVar()
        self.category_filter_combobox = ttk.Combobox(self.category_frame,
                                                     values=['None', 'Ordinary', 'Pro'],
                                                     textvariable=self.category_filter_var,
                                                     state='readonly')
        self.category_filter_combobox.current(0)
        self.category_filter_combobox.bind('<<ComboboxSelected>>',
                                           lambda ev: self.handle_filter(ev, 'Category',
                                                                  self.category_filter_var.get()))

        self.cuisine_frame = tk.Frame(self.filters_frame)
        self.cuisine_filter_text = tk.Label(self.cuisine_frame, text="Cuisine", font=self.font)
        self.cuisine_filter_listbox = tk.Listbox(self.cuisine_frame, selectmode=tk.MULTIPLE,
                                                 height=4,
                                                 selectbackground='grey', relief=tk.FLAT,
                                                 highlightcolor='black',
                                                 exportselection=False)
        self.cuisine_filter_listbox.insert(tk.END, 'African', 'Continental', 'Arabian',
                                           'Chinese', 'Belgian', 'French',
                                           'North Indian', 'South Indian')

        self.cuisine_filter_listbox.bind('<Button-1>', lambda ev: self.check_deselect(ev))

        self.active_filter = {}
        for col in self.data.get_cols():
            self.active_filter[col] = ''

    def component_install(self):
        self.table.pack(side=tk.LEFT, fill=tk.Y)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)

        self.filter_text.grid(column=1, row=0, sticky=tk.W)

        self.quantity_frame.grid(column=1, row=1, padx=20)
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

        self.zone_frame.grid(column=3, row=2)
        self.zone_filter_text.pack()
        self.zone_filter_listbox.pack()

        self.restaurant_frame.grid(column=1, row=3)
        self.restaurant_filter_text.pack()
        self.restaurant_filter_combobox.pack()

        self.category_frame.grid(column=2, row=3)
        self.category_filter_text.pack()
        self.category_filter_combobox.pack()

        self.cuisine_frame.grid(column=3, row=3)
        self.cuisine_filter_text.pack()
        self.cuisine_filter_listbox.pack()

        self.filters_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def table_col_config(self):
        for i, col in enumerate(self.data.get_cols()):
            self.table.heading('#' + str(i), text=col)

        self.table.column('#0', minwidth=0, stretch=True)

        optimal_width = int(self.root.winfo_screenwidth() / 18)

        for col_num in range(2, len(self.data.get_cols())):
            self.table.column('#' + str(col_num), minwidth=0, width=optimal_width, stretch=False)

    def grid_config(self):
        # self.filters_frame.columnconfigure(0, weight=1, uniform=True)
        self.filters_frame.columnconfigure(1, weight=1, uniform=True)
        self.filters_frame.columnconfigure(2, weight=1, uniform=True)
        self.filters_frame.columnconfigure(3, weight=1, uniform=True)
        # self.filters_frame.columnconfigure(4, weight=1, uniform=True)

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

    def check_deselect(self, ev):
        self.root.after(5, lambda ev=ev: self.handle_listbox(ev))

    def handle_listbox(self, ev):
        filter = []
        listbox = ev.widget

        match listbox:
            case self.payment_filter_listbox:
                col = 'Payment Mode'
                label = self.payment_filter_text
            case self.zone_filter_listbox:
                col = 'Zone'
                label = self.zone_filter_text
            case self.cuisine_filter_listbox:
                col = 'Cuisine'
                label = self.cuisine_filter_text

        values = self.data.get_unique_val(col)

        for i in listbox.curselection():
            filter.append(listbox.get(i))
        match len(filter):
            case 2:
                self.active_filter[col] = [','.join(filter), 'multexact']
            case 1:
                self.active_filter[col] = [filter[0], 'exact']
            case 0:
                self.active_filter[col] = [','.join(values), 'multexact']
                label.config(fg='white')
                self.refresh_data()
                return
            case _:
                self.active_filter[col] = [','.join(filter), 'multexact']

        label.config(fg='yellow')
        self.refresh_data()

    def handle_filter(self, event, col, filter):
        if filter in ['', 'None']:
            self.reset_filter(event)
            self.active_filter[col] = ''
            self.refresh_data()
            return

        if ',' in filter and '-' in filter:
            messagebox.showerror('INVALID FILTER VALUES', 'Value Error: Must be in format "A-B" or "A"\n')
            return

        # Check nominal value filter
        if col in self.data.get_nominal_cols():
            if ',' in filter:
                filters = filter.split(',')
                valid_cols = self.data.get_unique_val(col)
                if not all(c in valid_cols for c in filters):
                    messagebox.showerror('INVALID FILTER VALUES',
                                         'Value Error: All values in the filter must be in the data\n')
                    return
                mode = 'multexact'
            else:
                if filter not in self.data.get_unique_val(col):
                    messagebox.showerror('INVALID FILTER VALUE',
                                         'Value Error: Filter value must be in the data')
                    return
                mode = 'exact'

        # Check numerical value filter (must be integer)
        elif col in self.data.get_numerical_cols():
            if '-' in filter:
                filters = filter.split('-')
                if not all(c.isdigit() for c in filters):
                    messagebox.showerror('INVALID FILTER VALUES',
                                         'Type Error: Filter value must be integer')
                    return
                mode = 'range'
            else:
                if not filter.isdigit():
                    messagebox.showerror('INVALID FILTER VALUES',
                                         'Type Error: Filter value must be integer')
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

        self.restaurant_button = tk.Button(self.selection_frame, text="Restaurant Name", bg="Black",
                                           command=lambda: self.handle_graph('Restaurant Name'))
        self.cuisine_button = tk.Button(self.selection_frame, text="Cuisine", bg="Black",
                                        command=lambda: self.handle_graph('Cuisine'))
        self.zone_button = tk.Button(self.selection_frame, text="Zone", bg="Black",
                                     command=lambda: self.handle_graph('Zone'))
        self.category_button = tk.Button(self.selection_frame, text="Category", bg="Black",
                                         command=lambda: self.handle_graph('Category'))
        self.payment_button = tk.Button(self.selection_frame, text="Payment Mode", bg="Black",
                                        command=lambda: self.handle_graph('Payment Mode'))
        self.quantity_button = tk.Button(self.selection_frame, text="Quantity of Items", bg="Black",
                                         command=lambda: self.handle_graph('Quantity of Items'))
        self.delivery_button = tk.Button(self.selection_frame, text="Delivery Time", bg="Black",
                                         command=lambda: self.handle_graph('Delivery Time'))
        self.food_rate_button = tk.Button(self.selection_frame, text="Food Rating", bg="Black",
                                          command=lambda: self.handle_graph('Food Rating'))
        self.deli_rate_button = tk.Button(self.selection_frame, text="Delivery Rating", bg="Black",
                                          command=lambda: self.handle_graph('Delivery Rating'))

        self.density_var = tk.BooleanVar()
        self.density_toggle = ttk.Checkbutton(self.selection_frame, variable=self.density_var, text='Density',
                                              onvalue=True, offvalue=False, command=lambda: self.handle_graph(-99))

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

        self.selection_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1, uniform=True)
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
        self.bar_config_combobox = ttk.Combobox(self.config_frame, values=self.data.get_nominal_cols(),
                                                state='readonly')
        self.bar_config_combobox.current(0)
        self.bar_config_combobox.bind('<<ComboboxSelected>>', self.handle_graph)

        self.height_config_text = ttk.Label(self.config_frame, text="Height")
        self.height_config_combobox = ttk.Combobox(self.config_frame, values=self.data.get_numerical_cols(),
                                                   state='readonly')
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
        self.columnconfigure(0, weight=3, uniform=True)
        self.columnconfigure(1, weight=2, uniform=True)

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
        self.data.bar_graph(self.bar_config_combobox.get(), self.height_config_combobox.get(),
                            self.values_config_combobox.get())
        self.graph_img.draw()


class Story_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)

    def component_init(self):
        self.graph_frame = ttk.Frame(self)

        sct_img = self.create_image('scatter.png')
        self.graph_img = tk.Label(self.graph_frame, image=sct_img)
        self.graph_img.image = sct_img

        sct_img2 = self.create_image('scatter2.png')
        self.graph_img2 = tk.Label(self.graph_frame, image=sct_img2)
        self.graph_img2.image = sct_img2

        description = ('The correlation coefficient of Quantity of Items and Cost are 0.7004\n'
                       'This means that the higher the quantity of items are, the higher cost the order will be.\n'
                       'The reverse holds true as well, The higher the cost of an order is, '
                       'the more quantity of items there will be.')

        self.desc_frame = ttk.Frame(self)

        path = os.path.join(os.getcwd(), 'img', "correl.png")
        img = Image.open(path)
        img = img.resize((800, 100))
        correl_img = ImageTk.PhotoImage(img)
        self.correl_img = tk.Label(self.desc_frame, image=correl_img)
        self.correl_img.image = correl_img

        self.description = tk.Label(self.desc_frame, text=description, fg='white', font=('Arial', 14))

    def component_install(self):
        self.graph_img.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.graph_img2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.graph_frame.grid(column=1, row=0, padx=50, pady=50)

        self.correl_img.grid(sticky=tk.SE)
        self.description.grid(sticky=tk.NE)
        self.desc_frame.grid(column=2, row=0)

    def grid_config(self):
        self.columnconfigure(0, weight=1, uniform=True)
        self.columnconfigure(1, weight=1, uniform=True)
        self.columnconfigure(2, weight=1, uniform=True)
        self.rowconfigure(0, weight=1, uniform=True)

    def create_image(self, img_name):
        path = os.path.join(os.getcwd(), 'img', img_name)
        img = Image.open(path)
        w, h = img.size
        aspect_ratio = w / h
        ratio = 2.5
        height = self.root.winfo_screenheight() / ratio
        width = height * aspect_ratio
        size = int(width), int(height)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)


class Descriptive_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)

    def component_init(self):
        self.attribute_var = tk.StringVar()
        self.attribute_select = ttk.Combobox(self, textvariable=self.attribute_var,
                                             values=self.data.get_numerical_cols(), state='readonly')
        self.attribute_select.current(0)
        self.attribute_select.bind('<<ComboboxSelected>>', lambda ev: self.handle_combobox())

        self.stat_var = tk.StringVar()
        self.stat_label = tk.Label(self, font=('Arial', 14), textvariable=self.stat_var)

        self.grid_config()

        self.handle_combobox()

    def component_install(self):
        self.attribute_select.grid(column=0, row=0, sticky=tk.S)
        self.stat_label.grid(column=0, row=1, sticky=tk.N)

    def grid_config(self):
        self.columnconfigure(0, weight=1, uniform=True)

        self.rowconfigure(0, weight=2, uniform=True)
        self.rowconfigure(1, weight=3, uniform=True)

    def handle_combobox(self):
        self.stat_label.focus_force()
        col = self.attribute_var.get()
        stat = self.data.descriptive(col)
        self.stat_var.set(('Count : {}\n'
                           'Mean : {}\n'
                           'Std : {}\n'
                           'Min : {}\n'
                           'Max : {}\n'
                           'Q1 : {}\n'
                           'Q3 : {}\n'
                           'IQR : {}\n').format(*stat))
        current = self.attribute_select.current()


class About_Tab(New_Tab):
    def __init__(self, root):
        super().__init__(root)
        self.data_source = "https://www.kaggle.com/datasets/mohamedharris/restaurant-order-details\n"
        self.proposal = "https://docs.google.com/document/d/1saBdR1z_1J8v7o5Eu1hJuhFq35pFtAGzNEH_F-Dq998"

    def component_init(self):
        desc = ("Food Data Visualizer was made to help user visualize\n"
                "and analyze people's behavior when choosing and ordering food.\n"
                "This program lets user be able to : \n"
                "Filter and view data, Create and analyze histograms, Create and analyze bar graphs, \n"
                "See an example data story, Analyze descriptive statistics\n"
                "Data attributes consists of \n"
                "Restaurant Name,Cuisine,Zone,Category,Payment Mode,Quantity of Items,\n"
                "Cost,Delivery Time,Food Rating, and Delivery Rating.\n\n"
                "The names of the restaurants used are only for representational purposes.\n"
                "They do not represent any real life nouns, but are only fictional.\n")

        self.desc_frame = ttk.Frame(self)

        self.desc_label = ttk.Label(self.desc_frame, text=desc, font=('Arial', 15))

        self.button_frame = ttk.Frame(self)
        self.source_button = ttk.Button(self.button_frame, text="Data Source",
                                        command=lambda: self.callback(self.data_source))
        self.proposal_button = ttk.Button(self.button_frame, text="Proposal",
                                          command=lambda: self.callback(self.proposal))

        self.grid_config()

    def component_install(self):
        self.desc_label.grid(column=0, row=0, sticky=tk.S, padx=20)
        self.desc_frame.grid(column=0, row=0, sticky=tk.S)

        self.source_button.grid(column=0, row=0, sticky=tk.N, padx=20)
        self.proposal_button.grid(column=1, row=0, sticky=tk.N, padx=20)
        self.button_frame.grid(column=0, row=1, sticky=tk.N)

    def grid_config(self):
        self.columnconfigure(0, weight=1, uniform=True)
        self.rowconfigure((0, 1), weight=1, uniform=True)

        self.button_frame.columnconfigure((0, 1, 2), weight=1, uniform=True)
        self.button_frame.rowconfigure(0, weight=1, uniform=True)

    def callback(self, url):
        webbrowser.open_new(url)


if __name__ == '__main__':
    root = tk.Tk()
    ui = UI(root)
    ui.run()
