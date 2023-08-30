from elreda.uis import GUI_V1, GUI
from elreda.services import OrderService
from playsound import playsound
from kink import inject
from datetime import date

@inject
class GUI_V2(GUI_V1):
    def __init__(self, _order_service: OrderService):
        super().__init__(_order_service)

    def start(self):
        super().start()

    def order_tab_ui(self):
        super().order_tab_ui()

    def get_date(self):
        today = date.today()
        date_today = today.strftime("%m/%d/%y")
        return date_today

    def root_tab(self):
        super().root_tab()

    def kitchen_busy_notification(self):
        super().kitchen_busy_notification()

    def kitchen_busy_notification_off(self):
        super().kitchen_busy_notification_off()

    def kitchen_tab_ui(self):
        super().kitchen_tab_ui()

    def submit_order(self):
        super().submit_order()
        playsound('bell-ring.wav')
        print("playing sound using soundplay")

    def check_order_queue(self):
        super().check_order_queue()

    def order_finished(self):
        super().order_finished()

    def new_order_kitchen_label(self):
        super().new_order_kitchen_label()

    def create_kitchen_tab(self):
        super().create_kitchen_tab()

    def report_tab_ui(self):
        super().report_tab_ui()

    def display_report_drink(self, _drink, _drink_qty):
        super().display_report_drink(_drink, _drink_qty)

    def display_report_food(self, _food, _food_qty):
        super().display_report_food(_food, _food_qty)

    def show_today_report(self):
        super().show_today_report()

    def recreate_report_tab(self):
        super().recreate_report_tab()

    def get_report_by_date(self, date_entry):
        super().get_report_by_date(date_entry)


