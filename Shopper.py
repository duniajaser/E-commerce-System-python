from User import User


class Shopper(User):
    def __init__(self, id_num, username, date_of_birth, active, basket, order):
        super().__init__(id_num, username, date_of_birth, active)
        self.basket = basket
        self.order = order
        self.cost = {}
        self.total_cost = 0

    def __str__(self):
        return (f"Shopper ID: {self.id_num}\n"
                f"Shopper Name: {self.username}\n"
                f"Date of Birth: {self.date_of_birth}\n"
                f"Active: {self.active}\n"
                f"Basket: {self.basket}\n"
                f"Order: {self.order}\n")
