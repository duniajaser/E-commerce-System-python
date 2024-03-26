from Shopper import Shopper
from Admin import Admin
from datetime import datetime
from Order import Order
import main
from Product import Product
import json
orders = list()


def menu(user, products, users, product_categories):
    print("------------------------- Menu -------------------------")
    print("1) Add product.")
    print("2) Place an item on sale.")
    print("3) Update product.")
    print("4) Add a new user.")
    print("5) Update user.")
    print("6) Display all users.")
    print("7) List products.")
    print("8) List shoppers.")
    print("9) Add product to the basket.")
    print("10) Display basket.")
    print("11) Update basket.")
    print("12) Place order.")
    print("13) Execute order.")
    print("14) Save products to a file.")
    print("15) Save users to a text file.")
    print("16) Exit the program.")
    print("------------------------------------------")
    option = input("Enter your choice:")
    if option == "1":
        # Add product (admin-only)
        add_product(user, products, users, product_categories)
    elif option == "2":
        # Place an item on sale (admin-only)
        place_an_item_on_sale(user, products, users, product_categories)
    elif option == "3":
        # Update product (admin-onl
        update_product(user, products, users, product_categories)
    elif option == "4":
        # Add a new user (admin-only)
        add_new_user(user, products, users, product_categories)
    elif option == "5":
        # Update user (admin-only)
        update_user(user, products, users, product_categories)
    elif option == "6":
        # Display all users (admin-only)
        display_all_users(user, products, users, product_categories)
    elif option == "7":
        # List products(admin and shopper)
        list_products(user, products, users, product_categories)
    elif option == "8":
        # List shoppers(admin-only)
        list_shoppers(user, products, users, product_categories)
    elif option == "9":
        # Add product to the basket (shopper-only)
        add_product_to_the_basket(user, products, users, product_categories)
    elif option == "10":
        # Display basket(shopper - only)
        display_basket(user, products, users, product_categories)
        menu(user, products, users, product_categories)
    elif option == "11":
        # Update basket (shopper-only)
        update_basket(user, products, users, product_categories)
    elif option == "12":
        # Place order (shopper-only)
        place_order(user, products, users, product_categories)
    elif option == "13":
        # Execute order (admin-only)
        execute_order(user, products, users, product_categories)
    elif option == "14":
        # Save products to a file(admin - only)
        save_products_to_a_file(user, products, users, product_categories)
    elif option == "15":
        # Save users to a text file (admin-only)
        save_users_to_a_file(user, products, users, product_categories)
    elif option == "16":
        # Exit (admin and shopper)
        print("Thank you ^_^")
        exit()
    else:
        print("Invalid choice!")
        menu(user, products, users, product_categories)

def intro(users):
    print("E-commerce System!")
    print("----- Log in -----")
    user_id = input("Enter your ID:")
    while check_id_in_list(users, user_id) is False:
        print("Please check the ID!")
        user_id = input("Enter your ID:")
    user = find_object_by_id(users, user_id)
    if isinstance(user, Admin):
        print(f"Welcome Admin {user.username}")
    if isinstance(user, Shopper):
        print(f"Welcome Shopper {user.username}")
    return user


def check_id_in_list(list1, id_num):
    for obj in list1:
        if obj.id_num == id_num:
            return True
    return False


def find_object_by_id(list1, id_num):
    for obj in list1:
        if obj.id_num == id_num:
            return obj
    return None


def add_product_to_the_basket(user, products, users, product_categories):
    if isinstance(user, Shopper):
        print(f"Welcome Shopper {user.username}")
        print("------------------------------------------")
        for i in products:
            print(i)
            print("------------------------------------------")
        product_id = input("Enter product ID:")
        while check_id_in_list(products, product_id) is False:
            print("Please check the ID of the product!")
            product_id = input("Enter product ID:")
        wanted_product = find_object_by_id(products, product_id)
        number_of_items = int(input("Enter the number of items:"))
        print("------------------------------------------")
        available_items = wanted_product.inventory
        if available_items > 0:
            if number_of_items <= available_items:
                # wanted_product.inventory -= number_of_items
                user.basket[wanted_product.id_num] = number_of_items
            else:
                print(f"The maximum number of items available is {wanted_product.id_num}")
        else:
            print("The product is sold out!")
    else:
        print(f"You can not do this option {user.username}, because you are an admin!")
    menu(user, products, users, product_categories)


def display_basket(user, products, users, product_categories):
    if isinstance(user, Shopper):
        display_basket_info(user, products, users, product_categories)
    else:
        print(f"You can not do this option {user.username}, because you are an admin!")


def update_basket(user, products, users, product_categories):
    if isinstance(user, Shopper):
        print("Current Basket:")
        display_basket_info(user, products, users, product_categories)
        print("1) Clear basket.")
        print("2) Remove basket.")
        print("3) Update basket.")
        print("------------------------------------------")
        option = input("Enter your choice:")
        if option == "1":
            user.basket = {}
            user.cost = {}
            user.total_cost = 0
        elif option == "2":
            remove_pro_id = input("Enter the Id of the product you want to remove:")
            while remove_pro_id not in user.basket:
                print("Please check the id:")
                remove_pro_id = input("Enter the Id of the product you want to remove:")
            user.basket.pop(remove_pro_id)
            cost_of_removed_product = user.cost.pop(remove_pro_id)
            user.total_cost -= cost_of_removed_product
            print("The product is removed!")
        elif option == "3":
            update_product_num_items = input("Enter the Id of the product you want to update:")
            while update_product_num_items not in user.basket:
                print("Please check the id:")
                update_product_num_items = input("Enter the Id of the product you want to update:")
            user.total_cost -= user.cost[update_product_num_items]
            new_num_items = int(input("Enter the new number of items:"))
            user.basket[update_product_num_items] = new_num_items
            product = find_object_by_id(products, update_product_num_items)
            current = datetime.now().strftime('%d/%m/%Y')
            if (product.has_an_offer == 1 and
                    product.valid_until >= current):
                user.cost[product.id_num] = new_num_items * product.offer_price
                user.total_cost += new_num_items * product.offer_price
            else:
                user.cost[product.id_num] = new_num_items * product.price
                user.total_cost += new_num_items * product.price
        else:
            print("Invalid choice!")
            update_basket(user, products, users, product_categories)
    else:
        print(f"You can not do this option {user.username}, because you are an admin!")
    menu(user, products, users, product_categories)


def display_basket_info(user, products,  users, product_categories):
    for pro in products:
        if pro.id_num in user.basket:
            num_of_items = user.basket[pro.id_num]
            print(pro)
            print(f"Number of items: {num_of_items}")
            print(f"Cost of purchase of the product: {user.cost[pro.id_num]}\n")
    print(f"Basket Cost =  {user.total_cost}\n")


def place_order(user, products, users, product_categories):
    if isinstance(user, Shopper):
        if not user.basket:
            print("Your basket is empty. Add items before placing an order.")
            return
        print("Your basket:")
        display_basket_info(user, products, users, product_categories)

        print("------------------------------------------")
        confirmation = input("Confirm order (yes/no): ")
        if confirmation.lower() == "yes":
            user.order = 1
            print("Order placed successfully!")
        else:
            print("Order not placed.")
    else:
        print(f"You can not do this option {user.username}, because you are an admin!")
    menu(user, products, users, product_categories)


def execute_order(user, products, users, product_categories):
    if isinstance(user, Admin):
        print("------------------------------------------")
        print(f"Welcome Admin {user.username}")
        user_id = int(input("Enter user id: "))
        while check_id_in_list(users, user_id) is False:
            print("Please check the ID!")
            user_id = input("Enter your ID:")
        shopp = find_object_by_id(users, user_id)
        for product_id, num_of_items in shopp.basket.items():
            for product in products:
                if product.id_num == product_id:
                    if product.inventory - num_of_items >= 0:
                        product.inventory -= num_of_items
                        order = Order(shopp, shopp.basket, shopp.cost)
                        orders.append(order)
                    else:
                        print(f"Insufficient quantity of {product.id_num} in stock for shopper {user.username}.")
        shopp.basket.clear()
        shopp.cost.clear()
        shopp.total_cost = 0
    else:
        print(f"You can not do this option {user.username}, because you are an Shopper!")
    menu(user, products, users, product_categories)


def list_shoppers(user, products, users, product_categories):
    if isinstance(user, Admin):
        print("------------------------------------------")
        print("1) List all shoppers.")
        print("2) List all shoppers that have added products for purchase to the basket.")
        print("3) List all shoppers that have an order that needs to be processed.")
        print("-------------------------------------------")
        option1 = input("Enter your choice:")
        if option1 == "1":
            for i in users:
                if isinstance(i, Shopper):
                    print(i)
                    print("------------------------------------------")
        elif option1 == "2":
            for i in users:
                if isinstance(i, Shopper):
                    if len(i.basket) != 0:
                        print(i)
                        print("------------------------------------------")
        elif option1 == "3":
            for i in users:
                if isinstance(i, Shopper):
                    if i.order == 1:
                        print(i)
                        print("------------------------------------------")
        else:
            print("Invalid choice!")
            list_shoppers(user, products, users, product_categories)
    else:
        print(f"You can not do this option {user.username}, because you are an Shopper!")
    menu(user, products, users, product_categories)


def list_products(user, products, users, product_categories):
    print("------------------------------------------")
    print("1) List all products.")
    print("2) List all products that have discount.")
    print("3) List products according to category.")
    print("4) List products according to product name.")
    print("------------------------------------------")
    option = input("Enter your choice:")
    if option == "1":
        for i in products:
            print(i)
            print("------------------------------------------")
    elif option == "2":
        for i in products:
            if i.has_an_offer == 1:
                print(i)
                print("------------------------------------------")

    elif option == "3":
        cat = input("Enter the name of category:")
        success = False
        element_list = list(product_categories.get_categories())
        for j in products:
            if j.category.upper() == cat.upper():
                print(j)
                success = True
                print("------------------------------------------")
        if success is False:
            print("There is no product with this category")
    elif option == "4":
        name = input("Enter the product name:")
        success = False
        for i in products:
            if i.name.upper() == name.upper():
                success = True
                print(i)
                print("------------------------------------------")
        if success is False:
            print("There is no product with this name")
    else:
        print("Invalid choice!")
        list_products(user, products, users, product_categories)

    menu(user, products, users, product_categories)


def save_users_to_a_file(user, products, users, product_categories):
    if isinstance(user, Admin):
        filename = str(input("Enter name of file.txt to save users on it:"))
        file_open = open(filename, 'w')
        for i in users:
            file_open.write(str(i.__str__()) + '\n')
        file_open.close()
    else:
        print(f"You can not do this option {user.username}, because you are an Shopper!")
    menu(user, products, users, product_categories)


def save_products_to_a_file(user, products, users, product_categories):
    if isinstance(user, Admin):
        filename = str(input("Enter name of file.txt to save products on it:"))
        file_open = open(filename, 'w')
        for i in products:
            file_open.write(str(i.__str__()) + '\n')
        file_open.close()
    else:
        print(f"You can not do this option {user.username}, because you are an Shopper!")
    menu(user, products, users, product_categories)


def add_product(user, products, users, product_categories):
    if isinstance(user, Admin):
        try:
            product_id = input("Enter product ID:")
            while check_id_in_list(products, product_id) is True:
                if main.is_id_6_digits(product_id) == 1:
                    print("Invalid ID (ID must be a 6 digits!")
                print("Please check the ID!")
                product_id = input("Enter product ID:")
            product_name = input("Enter name of product to be added: ")
            product_category = input("Enter Product category: ")
            product_categories.add_category(product_category)
            price = int(input("Enter Price: "))
            inventory = int(input("Enter Inventory: "))
            supplier = input("Enter Supplier: ")
            has_on_offer = int(input("Enter 1 if the product has an offer or 0 if the product has no offer: "))

            if has_on_offer == 1:
                offer_price = int(input("Enter offer price: "))
                valid_until = input("Enter the date the offer is valid (Day/Month/Year): ")
                valid_until = datetime.strptime(valid_until, '%d/%m/%Y')
            else:
                offer_price = 0
                valid_until = "0/0/0"
            new_product = Product(product_id, product_name, product_category, price, inventory, supplier,
                                  has_on_offer, offer_price, valid_until, product_categories)
            products.append(new_product)
            print("Product added successfully!")
        except ValueError as ve:
            print(f"Error: {ve}")
        except KeyboardInterrupt as Ke:
            print(f"Error: {Ke}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"You cannot do this option, {user.username}, because you are a Shopper!")
    menu(user, products, users, product_categories)


def place_an_item_on_sale(user, products, users, product_categories):
    if isinstance(user, Admin):
        item_id = input("Enter product id: ")
        for index, pro in enumerate(products):
            if pro.id_num == item_id:
                product_location = index
                products[product_location].has_an_offer = 1
                offer_price = int(input("Enter new Offer Price:"))
                products[product_location].offer_price = offer_price

                valid_until = input("Enter the date the offer is valid (Day/Month/Year): ")
                valid_until = datetime.strptime(valid_until, '%d/%m/%Y')
                products[product_location].valid_until = valid_until

                print("Product Placed on sale successfully!")

    else:
        print(f"You cannot do this option, {user.username}, because you are a Shopper!")
    menu(user, products, users, product_categories)


def update_product(user, products, users, product_categories):
    if isinstance(user, Admin):
        try:
            product_id = input("Enter product id that do you want to update:")
            for index, pro in enumerate(products):
                if pro.id_num == product_id:
                    product_location = index
                    print(
                        "1.Product Name\n2.Category\n3.Price\n4.Inventory\n5.Supplier\n6.has_an_offer\n"
                        "7.Offer Price\n8.Valid Until\n")

                    prameter = int(input("Enter the number of field do you want to update:\n"))

                    if (prameter == 1):
                        new_name = str(input("Enter new name:"))
                        products[product_location].name = new_name
                    elif (prameter == 2):
                        new_category = str(input("Enter new category:"))
                        products[product_location].category = new_category

                    elif (prameter == 3):
                        new_price = int(input("Enter new Price:"))
                        products[product_location].price = new_price

                    elif (prameter == 4):
                        new_supplier = str(input("Enter new Supplier:"))
                        products[product_location].Supplier = new_supplier

                    elif (prameter == 5):
                        new_has_an_offer = int(input("Enter if has offered or not:"))
                        products[product_location].has_an_offer = new_has_an_offer

                    elif (prameter == 6):
                        new_offer_price = int(input("Enter new Offer Price:"))
                        products[product_location].offer_price = new_offer_price
                    elif (prameter == 7):
                        new_valid_until = int(input("Enter the new date the offer valid:"))
                        products[product_location].valid_until = new_valid_until
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"You cannot do this option, {user.username}, because you are a Shopper!")
    menu(user, products, users, product_categories)


def add_new_user(user, products, users, product_categories):
    if isinstance(user, Admin):
        try:
            user_id = input("Enter user ID:")
            while check_id_in_list(users, user_id) is True:
                if main.is_id_6_digits(user_id) == 1:
                    print("Invalid ID (ID must be a 6 digits!")
                print("Please check the ID!")
                user_id = input("Enter user ID:")
            user_name = input("Enter name of user: ")
            user_date_of_birth = input("Enter date of birth: ")
            user_date_of_birth = datetime.strptime(user_date_of_birth, '%d/%m/%Y')
            role = input("Enter Role(Shopper/Admin): ")

            active = int(input("Enter 1 for active user, otherwise not active: "))

            user_input = input("Enter a dictionary (in JSON format) {'product IDs': quantities}: ")
            basket = json.loads(user_input)  # Parse the user's input into a dictionary

            order = int(input("Enter 1 if the user finished adding items to the basket and wants to make an order,"
                              "otherwise 0: "))
            if role.lower() == "shopper":
                # id_num, username, date_of_birth, active, basket, order
                shopp = Shopper(user_id, user_name, user_date_of_birth, active, basket, order)
                users.append(shopp)
                print("new user added successfully!")
            if role.lower() == "admin":
                adm = Admin(user_id, user_name, user_date_of_birth, active, basket, order)
                users.append(adm)
                print("new user added successfully!")

        except ValueError as ve:
            print(f"Error: {ve}")
        except KeyboardInterrupt as Ke:
            print(f"Error: {Ke}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"You cannot do this option, {user.username}, because you are a Shopper!")
    menu(user, products, users, product_categories)


def display_all_users(user, products, users, product_categories):
    if isinstance(user, Admin):
        for i in users:
            print(i)
            print("------------------------------------------")
    else:
        print(f"You cannot do this option, {user.username}, because you are a Shopper!")
    menu(user, products, users, product_categories)


def update_user(user, products, users, product_categories):
    if isinstance(user, Admin):
        try:
            user_id = input("Enter user id that do you want to update information: ")
            for index, us in enumerate(users):
                if us.id_num == user_id:
                    user_location = index
                    print("1.User Name\n2.date of birth\n3.Role\n4.Basket\n5.Active\n6.Order\n")
                    parameter = int(input("Enter the number of field do you want to update:\n"))
                    if (parameter == 1):
                        new_name = input("Enter new name: ")
                        users[user_location].username = new_name
                    elif (parameter == 2):
                        new_date_of_birth1 = (input("Enter new date of birth (Day/Moth/Year): "))
                        new_date_of_birth = datetime.strptime(new_date_of_birth1, '%d/%m/%y')
                        users[user_location].date_of_birth = new_date_of_birth
                    elif (parameter == 3):
                        new_role = str(input("Enter Role(Shopper/Admin): "))
                        users[user_location].role = new_role
                    elif (parameter == 4):
                        user_input = input("Enter a dictionary (in JSON format) {'product IDs': quantities}: ")
                        basket = json.loads(user_input)  # Parse the user's input into a dictionary
                        users[user_location].basket = basket
                    elif (parameter == 5):
                        active = int(input("Enter 1 for active user, otherwise not active: "))
                        users[user_location].active = active
                    elif (parameter == 6):
                        order = int(input("Enter 1 if the user finished adding items to the basket and"
                                          " wants to make an order,otherwise 0: "))
                        users[user_location].order = order
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"You cannot do this option, {user.username}, because you are a Shopper!")
    menu(user, products, users, product_categories)
