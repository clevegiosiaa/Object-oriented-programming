from elreda import services


class MockKitchen(services.OrderService):
    def __init__(self) -> None:
        self.__orders = []
        
    def new_order(self, _order):
        self.__orders.append(_order)
    
    def order_queue(self):
        return self.__orders
    
    def __iter__(self):
        return iter(self.order_queue())
    

def test_should_show_a_new_add_order_in_kitchen():
    # Before test
    kitchen = MockKitchen()
    order = {"table_no": 1, 
                "food" : "Kubideh",
                "food_qty" : 2, 
                "drink" : "Ayran", 
                "drink_qty" : 3,
                "name": "Cleve Giosia Adryana"}
    
    # Test
    kitchen.new_order(order)

    # Expected result
    current = kitchen.order_queue()[0]
    expected = order
    
    assert current == expected, "Order was not added to queue."