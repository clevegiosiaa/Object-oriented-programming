from elreda import services, uis

class MockKitchen(services.OrderService):
    def __init__(self) -> None:
        self.__orders = [{}, {}, {}, {}, {}]
        
    def new_order(self, _order):
        self.__orders.append(_order)
    
    def order_queue(self):
        return self.__orders
    
    def __iter__(self):
        return iter(self.order_queue())
    
    
class MockUI(uis.GUI_V1):
    def __init__(self, _order_service):
        self.service = _order_service
    
    def kitchen_busy_notification(self):
        return "Kitchen Busy"
    
    def kitchen_busy_notification_off(self):
        return "Kitchen not Busy"
    
    # def order_finished(self):
    #     self.check_order_queue()
    def submit_order(self):
        return self.check_order_queue()
        
    
    def check_order_queue(self):
        order = self.service.order_queue()
        if len(order) > 5:
            return self.kitchen_busy_notification()
        return self.kitchen_busy_notification_off()
    

def test_should_show_warning_msg_if_more_than_5_in_queue():
    # Before test
    new_order = {}
    kitchen = MockKitchen()
    ui = MockUI(kitchen)
    
    # Test
    kitchen.new_order(new_order)
    status = ui.submit_order()

    # Expected result
    expected = 'Kitchen Busy'
    current = status

    assert current == expected, f"Expected {expected}, but got {current} instead."
    
    
    
    