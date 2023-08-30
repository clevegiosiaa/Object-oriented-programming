class OrderMenuDTO:
    def __init__(self, _order_menu=None):
        self.order_menu = _order_menu
        

class ReportDTO:
    def __init__(self, _food=None, _drink=None, _food_qty=None, _drink_qty=None):
        self.food = _food
        self.drink = _drink
        self.food_qty = _food_qty
        self.drink_qty = _drink_qty