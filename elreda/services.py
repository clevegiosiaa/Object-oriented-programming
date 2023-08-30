from abc import abstractmethod
from typing import List
from kink import inject
from elreda.dtos import OrderMenuDTO

from elreda.persistance import OrderDatabase



class Services:
    @abstractmethod
    def get_report_from_database_order_by_date(self, _selected_date):
        pass
    
    @abstractmethod
    def get_foods(self):
        pass
    
    @abstractmethod
    def get_drinks(self):
        pass
    
    @abstractmethod
    def new_order(self, _order):
        pass
    
    @abstractmethod
    def list_of_orders(self):
        pass
    
    @abstractmethod 
    def finish_order(self, _order):
        pass
    
    @abstractmethod   
    def order_queue(self):
        pass
    
    @abstractmethod
    def all_order_queue(self):
        pass
    
    @abstractmethod
    def insert_data_to_database(self, _order, _date):
        pass


class OrderNotification:
    @abstractmethod
    def notified(self, _type, _order):
        pass
    
    
@inject(alias=OrderNotification)
class Restaurant(OrderNotification):
    def notified(self, _type, _order):
        if _type == "BUSY":
            print("Kitchen is busy")
    

@inject(alias=OrderNotification)
class Customer(OrderNotification):
    def notified(self, _type, _order):
        if _type == "DONE":
            if _order != []:
                print()
                print("+"*40)
                print(f"Email sent to {_order['name']}")
                print(f"Order:")
                print(f"\t{_order['food']}\t{_order['food_qty']}")
                print(f"\t{_order['drink']}\t{_order['drink_qty']}")
                print("+"*40, "\n")
            else:
                print("Email not sent")


@inject(alias=OrderNotification)
class Kitchen(OrderNotification):
    def notified(self, _type, _order):
        if _type == "NEW_ORDER":
            print("New Order Created")

        elif _type == "DONE":
            print("Kitchen Order Done")




@inject
class Publisher:
    def __init__(self, _subscriber: List[OrderNotification]):
        self.subscriber = _subscriber
        
    def unsubscribe(self):
        if len(self.subscriber) > 0:
            self.subscriber.pop(0)
            
    def notify(self, _type, _order):
        for i in range(len(self.subscriber)):
            self.subscriber[i].notified(_type, _order)


@inject
class OrderService(Services):
    def __init__(self, _order_db: OrderDatabase, _publisher: Publisher):
        self.__order_db = _order_db
        self.__publisher = _publisher
        self.__order = []


    def initialise_new_database(self):
        self.__order_db.initialize_database()
        
    def init(self):
        pass
    
    def get_report_from_database_order_by_date(self, _selected_date):
        return self.__order_db.get_reports(_selected_date)
    
    def get_foods(self):
        return self.__order_db.get_foods_data()
    
    def get_drinks(self):
        return self.__order_db.get_drinks_data()
    
    def new_order(self, _order):
        self.__publisher.notify("NEW_ORDER", _order)
        self.__order.append(_order)
        self.list_of_orders()

    def list_of_orders(self):
        if len(self.__order) != 0:
            print("\n------------ LIST OF ORDERS ------------\n")
            for i in range(len(self.__order)):
                print("-"*40)
                print(f"Table: {self.__order[i]['table_no']}")
                print(f"Food: {self.__order[i]['food']}\t{self.__order[i]['food_qty']}")
                print(f"Drink: {self.__order[i]['drink']}\t{self.__order[i]['drink_qty']}")
                print("-"*40)
        else:
            print("No more order")
        
    def finish_order(self, _order):
        self.__publisher.notify("DONE", _order)
        # self.__publisher.unsubscribe()
        if len(self.__order) == 1:
            self.__order.pop()
        elif self.__order != []:
            self.__order.pop(0)
        elif self.__order == []:
            print("No more order that can be done\n")
        
    def order_queue(self):
        if len(self.__order) > 0:
            if len(self.__order) > 5:
                self.__publisher.notify("BUSY", None)
            return self.__order[0]
        return self.__order
    
    def all_order_queue(self):
        return self.__order
    
    def insert_data_to_database(self, _order, _date):
        return self.__order_db.insert_data(_order, _date)


    def __iter__(self):
        return iter(self.order_queue())
    

