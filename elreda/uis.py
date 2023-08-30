from kink import inject
from tkinter import *
from tkinter import ttk
from datetime import date
from abc import abstractmethod

from elreda.services import OrderService


class GUI:
    @abstractmethod
    def start(self):
        pass



@inject
class GUI_V1(GUI):
    def __init__(self, _order_service: OrderService):
        self.order_service = _order_service
        self.root = Tk()
        
    def init(self):
        pass

    def start(self):
        self.root.geometry("450x300")
        self.root.title("El Reda")

        title = Label(self.root, text="El Reda\nHuttenstraße 69-70,\n10553 Berlin, Germany", font=("Courier", 14))
        title.grid(row=0, column=0, columnspan=3)
        self.root_tab()

        self.notebook = ttk.Notebook(self.root)
        self.order_tab = Frame(self.notebook)
        self.kitchen_tab = Frame(self.notebook)
        self.report_tab = Frame(self.notebook)

        self.notebook.add(self.order_tab, text="Order")
        self.notebook.add(self.kitchen_tab, text="Kitchen")
        self.notebook.add(self.report_tab, text="Report")
        self.notebook.grid(row=2, column=0, columnspan=3)

        self.order_tab_ui()
        self.kitchen_tab_ui()
        self.report_tab_ui()

        self.root.mainloop()

    def order_tab_ui(self):
        # ##############################
        # ######### ORDER TAB ##########
        # ##############################
        self.food_label = Label(self.order_tab, text="Food              :", font=("Courier", 12), width=20, anchor='w')
        self.drink_label = Label(self.order_tab, text="Drink             :", font=("Courier", 12), width=20, anchor='w')
        self.table_number_label = Label(self.order_tab, text="Table Number      :", font=("Courier", 12), width=20, anchor='w')
        self.name_label = Label(self.order_tab, text="Customer Name     :", font=("Courier", 12), width=20, anchor='w')
        self.qty_label = Label(self.order_tab, text="Qty", font=("Courier", 11))
        self.qty_label.grid(row=0, column=2)
        self.food_label.grid(row=1, column=0)
        self.drink_label.grid(row=2, column=0)
        self.table_number_label.grid(row=3, column=0)
        self.name_label.grid(row=4, column=0)
        
        # food Option Menu
        self.foods_name = self.order_service.get_foods()
        self.foods = [menu.order_menu for menu in self.foods_name]
        self.menu_option = ttk.Combobox(self.order_tab, state='readonly', values=self.foods, width=20)
        self.menu_option.grid(row=1, column=1, padx=5)
        self.menu_qty_entry = Entry(self.order_tab, width=10)
        self.menu_qty_entry.grid(row=1, column=2, padx=5)
        
        # drink Option Menu
        self.drinks_name = self.order_service.get_drinks()
        self.drinks = [menu.order_menu for menu in self.drinks_name]
        self.drink_option = ttk.Combobox(self.order_tab, state='readonly', values=self.drinks, width=20)
        self.drink_option.grid(row=2, column=1, padx=5)
        self.drink_qty_entry = Entry(self.order_tab, width=10)
        self.drink_qty_entry.grid(row=2, column=2, padx=5)
        
        # table number entry
        self.table_number_entry = ttk.Combobox(self.order_tab, state='readonly', values=[str(i) for i in range(1, 13)], width=20)
        self.table_number_entry.grid(row=3, column=1, padx=5)
        
        # name entry
        self.name_entry = Entry(self.order_tab, width=20)
        self.name_entry.grid(row=4, column=1, padx=5)
        
        # order button
        self.order_button = Button(self.order_tab, text="ORDER", width=10, relief='solid', borderwidth=1, command=self.submit_order)
        self.order_button.grid(row=6, column=2, padx=5)
        
        self.check_order_queue()
        
        self.root.update()

    def get_date(self):
        today = date.today()
        date_today = today.strftime("%m/%d/%y")
        return date_today

    def root_tab(self):
        date_label = Label(self.root, text=self.get_date(), font=("Courier", 12))
        date_label.grid(row=1, column=2)

    def kitchen_busy_notification(self):
        self.busy_label = Label(self.order_tab, text="Kitchen is busy (remind guest!!)", font=("Courier", 11), fg="red", width=40)
        self.busy_label.grid(row=5, column=0, columnspan=2)
        self.root.update()
        
    def kitchen_busy_notification_off(self):
        self.busy_label = Label(self.order_tab, width=40)
        self.busy_label.grid(row=5, column=0, columnspan=2)
        self.root.update()
        
    def kitchen_tab_ui(self):
        # ##############################
        # ######### KITCHEN TAB ########
        # ##############################
        
        self.new_order_kitchen_label()

        self.root.update()
        
    def submit_order(self):
        table_number = self.table_number_entry.get()
        food = self.menu_option.get()
        food_qty = self.menu_qty_entry.get()
        drink = self.drink_option.get()
        drink_qty = self.drink_qty_entry.get()
        name = self.name_entry.get()
        
        self.order = {"table_no": table_number, 
                "food" : food,
                "food_qty" : food_qty, 
                "drink" : drink, 
                "drink_qty" : drink_qty,
                "name": name}
        
        self.order_service.new_order(self.order)
        
        self.check_order_queue()
            
        self.new_order_kitchen_label()
        
        # self.food_order_label()
        self.root.update()

    def check_order_queue(self):
        order = self.order_service.all_order_queue()
        if len(order) > 5:
            self.kitchen_busy_notification()
        else:
            self.kitchen_busy_notification_off()


    def order_finished(self):
        date = self.get_date()
        order = self.order_service.order_queue()
        self.order_service.list_of_orders()
        self.order_service.finish_order(order)
        self.check_order_queue()
        self.new_order_kitchen_label()
        if order != []:
            self.order_service.insert_data_to_database(order, date)

        self.order_tab.update()
        self.root.update()
        
    
    def new_order_kitchen_label(self):
        order = self.order_service.order_queue()

        self.create_kitchen_tab()

        if order != []:
            self.table_no_label = Label(self.kitchen_tab, text=order['table_no'], font=("Courier", 12), width=10, anchor='w').place(x=30, y=40)
            self.food_order_label = Label(self.kitchen_tab, text=order['food'], font=("Courier", 12), width=14, anchor='w').place(x=150, y=40)
            self.drink_label = Label(self.kitchen_tab, text=order['drink'], font=("Courier", 12), width=14, anchor='w').place(x=150, y=60)
            self.food_qty_label = Label(self.kitchen_tab, text=order['food_qty'], font=("Courier", 12), width=10, anchor='w').place(x=320, y=40)
            self.drink_qty_label = Label(self.kitchen_tab, text=order['drink_qty'], font=("Courier", 12), width=10, anchor='w').place(x=320, y=60)

    def create_kitchen_tab(self):
        for widgets in self.kitchen_tab.winfo_children():
            widgets.destroy()

        table_number_label = Label(self.kitchen_tab, text="Table No.", font=("Courier", 12), width=20, anchor='w')
        order_queue_label = Label(self.kitchen_tab, text="Order Queue", font=("Courier", 12), width=20, anchor='w')
        qty_label = Label(self.kitchen_tab, text="Qty", font=("Courier", 12), width=20, anchor='w')
        table_number_label.place(x=10, y=10)
        order_queue_label.place(x=150, y=10)
        qty_label.place(x=310, y=10)
        done_button = Button(self.kitchen_tab, text="DONE", width=10, relief='solid', borderwidth=1,
                             command=self.order_finished)
        done_button.place(x=360, y=115)

    def report_tab_ui(self):
        # ##############################
        # ######### REPORT TAB ######### 
        # ############################## 
        self.show_today_report()
        # self.display_report(report)
        date_entry = Entry(self.report_tab, font=("Courier", 12), width=10)
        date_entry.place(x=30, y=13)
        Button(self.report_tab, text="Search", command=lambda: self.get_report_by_date(date_entry)).place(x=140, y=10)
        Label(self.report_tab, text="Foods", font=("Courier", 12), width=10, anchor='w').place(x=30, y=40)
        Label(self.report_tab, text="Drinks", font=("Courier", 12), width=10, anchor='w').place(x=250, y=40)
        self.root.update()

    def display_report_food(self, _food, _food_qty):
        Label(self.report_tab, text=_food, font=("Courier", 12), width=14, anchor='w').place(x=30, y=self.y_food)
        Label(self.report_tab, text=_food_qty, font=("Courier", 12), width=2, anchor='w').place(x=170, y=self.y_food)
        self.y_food += 20

    def display_report_drink(self, _drink, _drink_qty):
            
        Label(self.report_tab, text=_drink, font=("Courier", 12), width=14, anchor='w').place(x=250, y=self.y_drink)
        Label(self.report_tab, text=_drink_qty, font=("Courier", 12), width=2, anchor='w').place(x=400, y=self.y_drink)
        self.y_drink += 20

    def show_today_report(self):
        date = self.get_date()
        self.report = self.order_service.get_report_from_database_order_by_date(date)
        
        self.orders_food = dict()
        self.orders_drink = dict()

        for data in self.report:
            if data.food != None:
                self.orders_food[data.food] = data.food_qty
            if data.drink != None:
                self.orders_drink[data.drink] = data.drink_qty

        self.y_food = self.y_drink = 60
        for key in self.orders_food:
            self.display_report_food(key, self.orders_food[key])
        for key in self.orders_drink:
            self.display_report_drink(key, self.orders_drink[key])

        self.report_tab.update()
        self.root.update()

    def recreate_report_tab(self):
        for widgets in self.report_tab.winfo_children():
            widgets.destroy()
            
        date_entry = Entry(self.report_tab, font=("Courier", 12), width=10)
        date_entry.place(x=30, y=13)
        Button(self.report_tab, text="Search", command=lambda: self.get_report_by_date(date_entry)).place(x=140, y=10)
        Label(self.report_tab, text="Foods", font=("Courier", 12), width=10, anchor='w').place(x=30, y=40)
        Label(self.report_tab, text="Drinks", font=("Courier", 12), width=10, anchor='w').place(x=250, y=40)

    def get_report_by_date(self, date_entry):
        print("#######################\nNew Report\n#######################")
        date = date_entry.get()
        self.recreate_report_tab()
        self.report = self.order_service.get_report_from_database_order_by_date(date)\
        
        if self.report != []:
            self.orders_food = dict()
            self.orders_drink = dict()

            for data in self.report:
                if data.food != None:
                    self.orders_food[data.food] = data.food_qty
                if data.drink != None:
                    self.orders_drink[data.drink] = data.drink_qty

            self.y_food = self.y_drink = 60
            for key in self.orders_food:
                self.display_report_food(key, self.orders_food[key])

            for key in self.orders_drink:
                self.display_report_drink(key, self.orders_drink[key])
        
        else:
            Label(self.report_tab, text="Data is unavailable", font=("Courier", 12), width=20, anchor='w', fg='red').place(x=30, y=self.y_food)
            
        
        self.report_tab.update()
        self.root.update()