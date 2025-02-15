class FoodWasteRecord:
    def __init__(self, date, amount_collected):
        self.date = date  # Store the date (YYYY-MM-DD)
        self.amount_collected = amount_collected  # Food waste collected in kg

    def get_amount(self):
        return self.amount_collected

    def get_date(self):
        return self.date
