import main2
from Product import Product
from Product import ProductCategoryManger
from Product import ProductCategory
from Shopper import Shopper
from Admin import Admin
from datetime import datetime


def read_products(products, product_categories):
    try:
        file_open = open('products.txt', 'r')
        for x in file_open:
            x1 = x.split(";")
            num = int(x1[0])
            if len(x1[0]) == 6:
                # Format the number as a string with leading zeros preserved
                id_num = f'{num:06}'
                if is_id_unq(id_num, products) == 0 and is_id_6_digits(id_num) == 0:
                    name = x1[1]
                    category = x1[2]
                    product_categories.add_category(category)
                    price = int(x1[3])
                    inventory = int(x1[4])
                    supplier = x1[5]
                    has_an_offer = int(x1[6])
                    if has_an_offer == 1:
                        offer_price = int(x1[7])
                        date1 = x1[8].strip()
                        d1 = date1.split("/")
                        day = int(d1[0])
                        month = int(d1[1])
                        year = int(d1[2])
                        valid_until = datetime(year, month, day)
                        formatted_date = valid_until.strftime("%d/%m/%Y")
                        product = Product(id_num, name, category, price, inventory, supplier, has_an_offer, offer_price,
                                          formatted_date, product_categories)
                        products.append(product)
                    else:
                        offer_price = int(x1[7])
                        date1 = x1[8].strip()
                        product = Product(id_num, name, category, price, inventory, supplier, has_an_offer, offer_price,
                                          date1, product_categories)
                        products.append(product)
            else:
                print(f"The id {x1[0]} is not accepted, it should ba a 6-digit unique code for the product")
                print("------------------------------------------")
        file_open.close()

    except IOError:
        print("Error, can not load the product file!")


def is_id_unq(id_num, lists):
    if id_num not in lists:
        return 0
    return 1


def is_id_6_digits(id_num):
    if str(id_num).isdigit() and len(str(id_num)) == 6:
        return 0
    return 1


def read_users(users, products):
    try:
        file_open = open('users.txt', 'r')
        for x1 in file_open:
            x = x1.split(";")
            name = x[1]
            d1 = x[2].split("/")
            day = int(d1[0])
            month = int(d1[1])
            year = int(d1[2])
            date_birth = datetime(year, month, day)
            formatted_date = date_birth.strftime("%d/%m/%Y")
            role = x[3]
            active = int(x[4])
            order = int(x[6].strip())
            if len(x[0]) == 6:
                num = int(x[0])
                # Format the number as a string with leading zeros preserved
                id_num = f'{num:06}'
                if is_id_unq(id_num, users) == 0 and is_id_6_digits(id_num) == 0:
                    if role.lower() == "shopper":
                        basket = basket_maker(x[5], products, id_num)
                        shopper = Shopper(id_num, name, formatted_date, active, basket, order)
                        users.append(shopper)
                    else:
                        admin = Admin(id_num, name, formatted_date, active, {}, 0)
                        users.append(admin)

            else:
                print(f"The id {x[0]} is not accepted, it should ba a 6-digit unique code for the user")
                print("------------------------------------------")
        for i in users:
            making_costs(i, products)
        file_open.close()
    except IOError:
        print("Error, can not load the users file!")


def basket_maker(x, products, id_num_user):
    # Remove the first and last characters
    dic = {}
    new_x = x[1:-1]
    products_num_of_items = new_x.split(",")
    for i in products_num_of_items:
        j = i.split(":")
        product_id = j[0]
        if main2.check_id_in_list(products, product_id) is True:
            num_of_items = int(j[1])
            dic[product_id] = num_of_items
        else:
            print(f"For user {id_num_user}, product {product_id} is not existed in the product list!")
            print("------------------------------------------")

    return dic


def making_costs(user, products):
    for product in products:
        if product.id_num in user.basket:
            num_of_items = user.basket[product.id_num]
            current = datetime.now().strftime('%d/%m/%Y')
            # offer price
            if (product.has_an_offer == 1 and
                    product.valid_until >= current):
                user.cost[product.id_num] = num_of_items * product.offer_price
                user.total_cost += num_of_items * product.offer_price
            else:
                user.cost[product.id_num] = num_of_items * product.price
                user.total_cost += num_of_items * product.price


def main():
    users = list()
    products = list()
    product_categories = ProductCategoryManger()
    product_categories.add_enum_categories(ProductCategory)
    read_products(products, product_categories)
    read_users(users, products)
    user = main2.intro(users)
    main2.menu(user, products, users, product_categories)


if __name__ == '__main__':
    main()
