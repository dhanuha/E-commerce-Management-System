'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023

This programme offers a system that is based on roles and serves both administrators and customers.
Access to features like product management, customer management, order management, data generation,
and statistical figure generation is available to administrators. Customers, on the other hand, can browse products,
view order history, generate consumption statistics, and search for products by ID in addition to viewing their profile
and updating their personal data.
The software makes sure that users can carry out actions that are related to their assigned roles.
'''

from io_interface import IOInterface
from operation_user import UserOperation
from operation_customer import CustomerOperation
from opreation_product import ProductOperation
from operation_order import OrderOperation
io = IOInterface()
uo = UserOperation()
co = CustomerOperation()
po = ProductOperation()
oo = OrderOperation()
# import the required libraries and necessary objects

def login_control():
    # controls the login process
    io.main_menu()
    choice = io.get_user_input("Please enter the corresponding value for the action you wish to take ", 1)[0]
    if choice == '1':
        # user Chose to login
        user_name = io.get_user_input("please enter the username : ", 1)[0]
        user_password = io.get_user_input("please enter the user password : ", 1)[0]
        user = uo.login(user_name, user_password)
        if user is not None:
            io.print_message("login successful")
            if user.user_role == 'customer':
                # checks if user is customer or admin by using user name and password and calls the customer control or admin control accordingly
                customer_control(user)
            elif user.user_role == 'admin':
                admin_control()
            else:
                io.print_error_message("user_operation", "user not found , please try again")
        else:
            io.print_error_message("login", " invalid credentials , please try again")
            return login_control()

    elif choice == '2':
        # user chose to register
        user_name = io.get_user_input("please enter the username : ", 1)[0]
        user_password = io.get_user_input("please enter the user password : ", 1)[0]
        user_email = io.get_user_input("please enter your email : ", 1)[0]
        user_mobile = io.get_user_input("please enter your mobile number : ", 1)[0]
        if co.register_customer(user_name, user_password, user_email, user_mobile):
            io.print_message("registration successful")
        else:
            io.print_error_message("Invalid format","registration unsuccessful change of format of details you entered")
        return login_control()


    elif choice == '3':
        # user chose to quit
        io.print_message("exiting the program")
    else:
        io.print_error_message("Choice", "Invalid Input , please try again choose either 1 or 2 or 3 ")
        return login_control()






def customer_control(user):
    while True:
        io.print_message("*** Welcome to the Customer Menu ***")
        # displays customer menu
        io.customer_menu()
        choice = io.get_user_input("please enter the corresponding value for the action u want to take : ", 1)[0]

        if choice == '1':
            # customer choose show profile
            user_name = user.user_name
            user_password = user.user_password
            customer = co.get_customer_prof(user_name, user_password)
            if customer is not None:
                cust_id = customer.user_id
                cust_name = customer.user_name
                cust_email = customer.user_email
                cust_mobile = customer.user_mobile
                io.print_message(f"customer_id : {cust_id}")
                io.print_message(f"Name : {cust_name}")
                io.print_message(f"email : {cust_email}")
                io.print_message(f"mobile : {cust_mobile}")
            else:
                io.print_error_message("Invalid Credentials", "the username or password is invalid, please retry")


        elif choice == '2':
            # customer choose update profile
            io.print_message("you have to enter your credentials again to update your profile")
            user_name = io.get_user_input("enter the a username : ", 1)[0]
            user_password = io.get_user_input("enter the password : ", 1)[0]
            io.print_message("attribute name should be name or password or email or mobile")
            attribute_name = str(io.get_user_input("enter the attribute name you want to change : ", 1)[0])
            value = io.get_user_input("enter the value of the attribute you want it to change : ", 1)[0]
            customer_object = co.get_customer_prof(user_name, user_password)
            if attribute_name in ['name', 'password', 'email', 'mobile']:
                if co.update_profile(attribute_name, value, customer_object):
                    io.print_message(f" Updating of {attribute_name} is successful")
                else:
                    io.print_error_message("invalid Format", f" Updating of {attribute_name} is failed")
            else:
                io.print_error_message("Attribute Name", "please enter a valid attribute name")


        elif choice == '3':
            # customer choose show products
            page_number = io.get_user_input("enter the page number to open that page of list : ", 1)[0]
            if page_number.isdigit():
                page_number = int(page_number)
                prod_list, page_num, total_pages = po.get_product_list(page_number)
                io.show_list('customer', 'Product', [prod_list, page_num, total_pages])
            else:
                io.print_error_message("Invalid Input", "please enter a valid page number")

        elif choice == '4':
            # customer chose show history orders
            customer_id = io.get_user_input("enter your customer id : ", 1)[0]
            page_number = io.get_user_input("enter the page number : ", 1)[0]
            if page_number.isdigit():
                page_number = int(page_number)
                order_list, page_num, total_pages = oo.get_order_list(customer_id, page_number)
                io.show_list('customer', 'Order', [order_list, page_num, total_pages])
            else:
                io.print_error_message("Invalid Input", "please enter a valid page number")

        elif choice == '5':
            # customer chose generate all consumption figures
            customer_id = io.get_user_input("enter your customer id : ", 1)[0]
            oo.generate_single_customer_consumption_figure(customer_id)
            oo.generate_all_customer_consumption_figure()
            oo.generate_all_top_10_best_sellers_figure()
            io.print_message("generation of all consumption figures successful")

        elif choice == '6':
            # customer choose get product by product id
            product_id = io.get_user_input("enter the product id of product you are looking for : ", 1)[0]
            if product_id.isdigit():
                product_id = int(product_id)
                product = po.get_product_by_id(product_id)
                if product is not None:
                    io.print_object(product)
                else:
                    io.print_error_message("Product Not Found", "there is no product with specified product id")
            else:
                io.print_error_message("Invalid Input", "please enter a valid product id")

        elif choice == '7':
            # customer choose to logout of customer menu
            io.print_message("logging out of customer menu")
            break

        else:
            io.print_error_message("Choice", "Invalid Input , please try again choose either 1 to 7 ")
        print()
    login_control()






def admin_control():
    while True:
        # opens the admin menu
        io.print_message("*** Welcome to the Admin Menu ***")
        io.admin_menu()
        choice = io.get_user_input("please enter the corresponding value for the action u want to take : ", 1)[0]
        if choice == '1':
            # admin choose show products
            page_number = io.get_user_input("please enter the desired product's page number : ", 1)[0]
            if page_number.isdigit():
                page_number = int(page_number)
                prod_list, page_number, total_pages = po.get_product_list(page_number)
                io.show_list('admin', 'Product', [prod_list, page_number, total_pages])
            else:
                io.print_error_message("Invalid Input", "please enter a valid page number")

        elif choice == '2':
            # admin chose to add customers
            user_name = io.get_user_input("please enter the username : ", 1)[0]
            user_password = io.get_user_input("please enter the user password : ", 1)[0]
            user_email = io.get_user_input("please enter your email : ", 1)[0]
            user_mobile = io.get_user_input("please enter your mobile number : ", 1)[0]
            registration = co.register_customer(user_name, user_password, user_email, user_mobile)
            if registration:
                io.print_message("registration successful")
            else:
                io.print_error_message("Registration Failed", "Please double-check the input formats and enter the information correctly")

        elif choice == '3':
            # admin chose to see customers list
            page_number = io.get_user_input("please enter the desired customer list's page number : ", 1)[0]
            if page_number.isdigit():
                page_number = int(page_number)
                cust_list, page_number, total_pages = co.get_customer_list(page_number)
                io.show_list('admin', 'Customer', [cust_list, page_number, total_pages])
            else:
                io.print_error_message("Invalid Input", "please enter a valid page number")

        elif choice == '4':
            # admin chose to see list of all orders
            page_number = io.get_user_input("enter the page number : ", 1)[0]
            if page_number.isdigit():
                page_number = int(page_number)
                order_list, page_num, total_pages = oo.get_all_order_list(page_number)
                io.show_list('admin', 'Order', [order_list, page_num, total_pages])
            else:
                io.print_error_message("Invalid Input", "please enter a valid page number")

        elif choice == '5':
            # admin chose to generate test data
            oo.generate_test_order_data()
            io.print_message("Test Data Generated Successfully")

        elif choice == '6':
            # admin chose to generate all statistical figures
            po.generate_category_figure()
            po.generate_discount_figure()
            po.generate_likes_count_figure()
            po.generate_discount_likes_count_figure()
            io.print_message("generation of all statistical figures successful")

        elif choice == '7':
            # admin chose to delete all the data
            io.print_message("all the data will we deleted and cant be reverted ")
            confirmation = io.get_user_input("type yes if you want to delete this data : ", 1)[0]
            if confirmation.lower() == 'yes':
                co.delete_all_customer()
                po.delete_all_product()
                oo.delete_all_orders()
                io.print_message("Deleted All The Data")
            else:
                io.print_message("Deletion of All The Data is cancelled")

        elif choice == '8':
            # admin chose to delete customer using customer id
            customer_id = io.get_user_input("enter the customer id of customer you want to delete : ", 1)[0]
            if co.delete_customer(customer_id):
                io.print_message(f"The customer with the customer_id : {customer_id} is successfully deleted.")
            else:
                io.print_error_message("Customer_id", f"The order with the order_id : {customer_id} is failed , please check customer id")

        elif choice == '9':
            # admin chose to delete order using order id
            order_id = io.get_user_input("enter the the order id of the order you want to delete  : ", 1)[0]
            if oo.delete_order(order_id):
                io.print_message(f"The order with the order_id : {order_id} is successfully deleted.")
            else:
                io.print_error_message("Order_id", f"The order with the order_id : {order_id} is failed , please check order id")

        elif choice == '10':
            # admin chose to delete product using product id
            product_id = io.get_user_input("enter the product id of product you want to delete : ", 1)[0]
            if product_id.isdigit():
                product_id = int(product_id)
                if po.delete_product(product_id):
                    io.print_message(f"The product with the product_id : {product_id} is successfully deleted.")
                else:
                    io.print_error_message("Product_id", f"The product with the product_id : {product_id} is not found , please check product id")
            else:
                io.print_error_message("Invalid Input", "please enter a valid page number")

        elif choice == '11':
            # admin chose to all products
            io.print_message("all the product data will we deleted and cant be reverted ")
            confirmation = io.get_user_input("type yes if you want to delete this data : ", 1)[0]
            if confirmation.lower() == 'yes':
                po.delete_all_product()
                io.print_message("Deleted All The products Data")
            else:
                io.print_message("Deletion of All products is cancelled")

        elif choice == '12':
            # admin chose to delete all orders
            io.print_message("all the order data will we deleted and cant be reverted ")
            confirmation = io.get_user_input("type 'yes' if you want to delete this data : ", 1)[0]
            if confirmation.lower() == 'yes':
                oo.delete_all_orders()
                io.print_message("Deleted All The order Data")
            else:
                io.print_message("Deletion of All The  order Data is cancelled")

        elif choice == '13':
            # admin chose to logout
            io.print_message("logging out of admin menu")
            break

        else:
            io.print_error_message("Choice", "Invalid Input , please try again choose from 1 to 13 ")
        print()
    login_control()

def main():
    login_control()


main()