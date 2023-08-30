
from elreda.persistance import OrderDB
from elreda.dtos import OrderMenuDTO, ReportDTO


class MockDB(OrderDB):
    def __init__(self):
        self.orders = [
            {"table_no": 1,
             "food": "Kubideh",
             "food_qty": 1,
             "drink": "Ayran",
             "drink_qty": 1,
             "date": "12/23/22"}
        ]

    
    def get_foods_data(self):
        foods_dto = []
        foods = ["Kubideh", "Sultani", "Fischteller", "Lammhaxe", "Tabbouleh"]
        for food in foods:
            foods_dto.append(OrderMenuDTO(food))

        return foods_dto
    
    def get_drinks_data(self):
        drinks_dto = []
        drinks = ["Ayran", "Boza", "Turkish Coffe", "Turkish Tea", "Turkish Raki"]
        for drink in drinks:
            drinks_dto.append(OrderMenuDTO(drink))
        return drinks_dto
        
    def insert_data(self, _order, _date):
        _order["date"] = _date
        self.orders.append(_order)
        
    def get_reports(self, _date):
        report_dto_list = []
        report_food = {}
        report_drink = {}
        for order in self.orders:
            if order['food'] not in report_food:
                report_food[order['food']] = order['food_qty']
            else:
                report_food[order['food']] += order['food_qty']
                
            if order['drink'] not in report_drink:
                report_drink[order['drink']] = order['drink_qty']
            else:
                report_drink[order['drink']] += order['drink_qty']

        for key in report_food:
            report_dto_list.append(ReportDTO(key, None, report_food[key], None))

        for key in report_drink:
            report_dto_list.append(ReportDTO(None, key, None, report_drink[key]))

        return report_dto_list