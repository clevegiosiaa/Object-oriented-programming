from elreda import services, uis


class MockCustomer(services.OrderNotification):
    def notified(self, _type, _order):
        if _type == "NEW_ORDER":
            if _order != []:
                return str("Email sent")
            else:
                return "Email not sent"
            
            
class MockPublisher(services.Publisher):
    def __init__(self, _subscriber):
        self.subscriber = [_subscriber]
    
    def notify(self, _type, _order):
        return self.subscriber[0].notified(_type, _order)
    
    
class MockKitchen(services.OrderService):
    def __init__(self) -> None:
        self.__orders = []
        self.__publisher = MockPublisher(MockCustomer())

    def new_order(self, _order):
        self.__orders.append(_order)
        return self.__publisher.notify("NEW_ORDER", _order)

    def list_of_orders(self):
        if len(self.__orders) != 0:
            return "Order queue printed"
        else:
            return "Order queue was not printed"

    def __iter__(self):
        return iter(self.order_queue())
    
    
class MockUI(uis.GUI_V1):
    def __init__(self, _service):
        self.service = _service
    
    def kitchen_busy_notification(self):
        return "Kitchen Busy"
    
    def kitchen_busy_notification_off(self):
        return "Kitchen not Busy"
    
    # def order_finished(self):
    #     self.check_order_queue()
    def submit_order(self, _order):
        return self.service.new_order(_order)


def test_email_sent_if_order_placed():
    # Before test
    order = {"table_no": 1, 
                "food" : "Kubideh",
                "food_qty" : 2, 
                "drink" : "Ayran", 
                "drink_qty" : 3,
                "name": "Cleve Giosia Adryana"}
    kitchen = MockKitchen()
    ui = MockUI(kitchen)
    
    # Test
    status = ui.submit_order(order)
    
    # Expected result
    current = status
    expected = "Email sent"
    assert current == expected, "Email was not sent."


def test_text_print_if_an_order_placed():
    # Before test
    order = {"table_no": 1, 
                "food" : "Kubideh",
                "food_qty" : 2, 
                "drink" : "Ayran", 
                "drink_qty" : 3,
                "name": "Cleve Giosia Adryana"}
    kitchen = MockKitchen()
    ui = MockUI(kitchen)

    # Test
    ui.submit_order(order)
    order_queue = kitchen.list_of_orders()

    #Expected result
    current = order_queue
    expected = "Order queue printed"
    assert current == expected, "Order queue was not printed if an was order placed."