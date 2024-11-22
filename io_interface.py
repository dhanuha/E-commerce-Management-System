'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

class IOInterface:
    def get_user_input(self, message,num_of_args):
        # get the user input and split it into list of different arguments
        user_input = input(message).split()
        result = user_input[:num_of_args]
        if len(user_input) < num_of_args:
            # if no.of args is more than args add empty string
            result.extend([''] * (num_of_args - len(result)))
        return result

    def main_menu(self):
        # display main menu
        print("Login Menu")
        print("1.Login")
        print("2.Register")
        print("3.Quit")

    def admin_menu(self):
        # display customer menu
        print("Admin Menu")
        print("1.Show Products")
        print("2.Add Customers")
        print("3.Show Customers")
        print("4.Show Orders")
        print("5.Generate test data")
        print("6.Generate statistical figures")
        print("7.Delete All Data")
        print("8.Delete Customer using customer_id")
        print("9.Delete order using order_id")
        print("10.Delete product using product_id")
        print("11.Delete All Products")
        print("12.Delete All Orders")
        print("13.Logout")


    def customer_menu(self):
        # display customer menu
        print("Customer Menu")
        print("1.Show Profile")
        print("2.Update Profile")
        print("3.Show Products")
        print("4.Show History orders")
        print("5.Generate all consumption figures")
        print("6.Get Product Using Product id")
        print("7.Logut")


    def show_list(self,user_role , list_type , object_list):
        # display a list of objects based on user role and list type
        if user_role == 'admin' or (user_role == 'customer' and list_type in ['Product','Order']):
            print(f"{list_type} List:")
            rows = object_list[0]
            page_number = object_list[1]
            total_pages = object_list[2]
            for i, obj in enumerate(rows, start =1):
                print(f"({i}) : {obj}")
            print(f"pagenum {page_number}/{total_pages}")
        else:
            print("you cant access this list")

    def print_error_message(self,error_source , error_message):
        # prints an error mesage with source
        print(f"ERROR in {error_source} : {error_message}")

    def print_message(self, message):
        # prints a  message
        print(message)

    def print_object(self,target_object):
        # prints the string representation of an object
        print(str(target_object))

