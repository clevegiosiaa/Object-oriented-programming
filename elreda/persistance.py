from abc import abstractmethod
import sqlite3
from sqlite3 import Error
from kink import inject

from elreda.dtos import OrderMenuDTO, ReportDTO

class OrderDB:
    @abstractmethod
    def get_foods_data(self):
        pass
    
    @abstractmethod
    def get_drinks_data(self):
        pass
    
    @abstractmethod
    def insert_data(self, _order, _date):
        pass
    
    @abstractmethod
    def get_reports(self, _date):
        pass
    


@inject
class OrderDatabase(OrderDB):
    def __init__(self, _db_setting):
        self.conn = self.connection(_db_setting)
        self.create_table()
        if self.conn is not None:
            self.c = self.conn.cursor()

    def connection(self, db_file):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return self.conn

    def create_table(self):
        pass


    def get_foods_data(self):
        menu_dtos = []
        query = "SELECT * FROM foods"
        self.c.execute(query)

        foods_data = self.c.fetchall()
        for id, menu in foods_data:
            menu_dtos.append(OrderMenuDTO(menu))
            
        return menu_dtos
    
    def get_drinks_data(self):
        menu_dtos = []
        query = "SELECT * FROM drinks"
        self.c.execute(query)

        drinks_data = self.c.fetchall()
        for id, menu in drinks_data:
            menu_dtos.append(OrderMenuDTO(menu))
            
        return menu_dtos

    def insert_data(self, _order, _date):
        self.c.execute("begin")

        food = _order['food']
        drink = _order['drink']
        self.c.execute("""SELECT food_id FROM foods WHERE food=?""", (food,))
        _food_id = self.c.fetchall()[0][0]
        self.c.execute("""SELECT drink_id FROM drinks WHERE drink=?""", (drink,))
        _drink_id = self.c.fetchall()[0][0]
        
        self.c.execute("INSERT INTO reports VALUES (:no, :food_id, :drink_id, :food_qty, :drink_qty, :date)",
            {'no' : None,
            'food_id' : _food_id,
            'drink_id' : _drink_id,
            'food_qty' : _order['food_qty'],
            'drink_qty' : _order['drink_qty'],
            'date' : _date
            })
        
        self.c.execute("commit")

    def get_reports(self, _date):
        report_dto_list = []
        self.c.execute("""SELECT  food_id FROM reports WHERE DATE=?""", (_date,))
        food_reports = self.c.fetchall()
        self.c.execute("""SELECT  drink_id FROM reports WHERE DATE=?""", (_date,))
        drink_reports = self.c.fetchall()

        for food in food_reports:
            food_id = food[0]

            self.c.execute("SELECT food FROM foods WHERE food_id=?", (food_id,))
            food = self.c.fetchall()[0]
            self.c.execute("SELECT SUM(food_qty) FROM reports WHERE food_id=? AND DATE=?", (food_id, _date,))
            food_qty = self.c.fetchall()[0]

            new_dto = ReportDTO(food, None, food_qty, None)
            report_dto_list.append(new_dto)

        for drink in drink_reports:
            drink_id = drink[0]

            self.c.execute("SELECT drink FROM drinks WHERE drink_id=?", (drink_id,))
            drink = self.c.fetchall()[0]
            self.c.execute("SELECT SUM(drink_qty) FROM reports WHERE drink_id=? AND DATE=?", (drink_id, _date,))
            drink_qty = self.c.fetchall()[0]

            new_dto = ReportDTO(None, drink, None, drink_qty)
            report_dto_list.append(new_dto)

        return report_dto_list
        
    def initialize_database(self):
        self.c.execute("DROP TABLE reports")
        self.c.execute("""
        CREATE TABLE reports (
        no INTEGER PRIMARY KEY AUTOINCREMENT,
        food_id text,
        drink_id text,
        food_qty integer,
        drink_qty integer,
        date text,
        FOREIGN KEY(food_id) REFERENCES food(food_id),
        FOREIGN KEY(drink_id) REFERENCES drink(drink_id)
        )
        """)
