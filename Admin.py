from User import User


class Admin(User):
    def __init__(self, id_num, username, date_of_birth, active, basket, order):
        super().__init__(id_num, username, date_of_birth, active)
        self.basket = basket
        self.order = order

    def __str__(self):
        return (f"Admin ID: {self.id_num}\n"
                f"Admin Name: {self.username}\n"
                f"Date of Birth: {self.date_of_birth}\n"
                f"Active: {self.active}\n")
