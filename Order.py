from datetime import datetime


class Order:
    def __init__(self, shopper, basket, total_cost):
        self.shopper = shopper
        self.basket = basket
        self.total_cost = total_cost
        self.timestamp = datetime.now()
