
        self.date_entry = Entry(self.report_tab, font=("Courier", 12), width=10).place(x=30, y=13) 
        # self.date_entry.insert(0, self.get_date())
        self.confirm_button = Button(self.report_tab, text="Search").place(x=140, y=10)
        self.food_label = Label(self.report_tab, text=self.report[0].food, font=("Courier", 12), width=10, anchor='w').place(x=30, y=50)
        self.drink_label = Label(self.report_tab, text=self.report[0].drink, font=("Courier", 12), width=10, anchor='w').place(x=30, y=70)
        self.food_qty_label = Label(self.report_tab, text=self.report[0].food_qty, font=("Courier", 12), width=10,