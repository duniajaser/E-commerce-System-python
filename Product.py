from enum import Enum


class Product:

    def __init__(self, id_num, name, category, price, inventory, supplier, has_an_offer, offer_price, valid_until,
                 product_categories):
        self.name = name
        self.id_num = id_num
        if category in ProductCategoryManger.get_categories(product_categories):
            self.category = category
        self.price = price
        self.supplier = supplier
        self.has_an_offer = has_an_offer
        self.inventory = inventory
        self.offer_price = offer_price
        self.valid_until = valid_until

    def __str__(self):
        return (f"Product ID: {self.id_num}\n"
                f"Product Name: {self.name}\n"
                f"Product Category: {self.category}\n"
                f"Price: {self.price}\n"
                f"Inventory: {self.inventory}\n"
                f"Supplier: {self.supplier}\n"
                f"has_an_offer: {self.has_an_offer}\n"
                f"Offer Price: {self.offer_price}\n"
                f"Valid Until: {self.valid_until}")


class ProductCategory(Enum):
    CLOTHES = "clothes"
    BEAUTY = "beauty"
    SHOES = "shoes"
    ELECTRONICS = "electronics"
    BOOKS = "books"


class ProductCategoryManger:
    def __init__(self):
        self.categories = set()

    def get_categories(self):
        return self.categories

    def add_category(self, category_name):
        if category_name.upper() not in self.categories:
            self.categories.add(category_name)

    def add_enum_categories(self, enum_class):
        for enum_member in enum_class:
            self.add_category(enum_member.name)

    def list_category_names(self):
        return list(self.categories)
