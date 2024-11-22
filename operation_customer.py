'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

import re
from operation_user import UserOperation
from model_customer import Customer
import time
uo = UserOperation()
class CustomerOperation:
    def validate_email(self, user_email):
        # checks the email with pattern
        pattern = r'^[\w.-]+@[a-zA-Z_-]+\.[a-zA-Z.]{2,}$'
        # match the email with pattern
        if re.match(pattern, user_email):
            return True
        else:
            return False


    def validate_mobile(self, user_mobile):
        # checks the length of mobile num is 10
        if len(user_mobile) != 10:
            return False
        # checks if the mobile num has only numbers and starts with either 03 or 04
        elif user_mobile.isdigit() and (user_mobile.startswith("04") or user_mobile.startswith("03")):
            return True
        else:
            return False



    def register_customer(self, user_name, user_password, user_email, user_mobile):
        uo = UserOperation()
        # validates username , user password, user email and user mobile
        if not all([user_name, user_password, user_email, user_mobile]):
            return False
        if not CustomerOperation.validate_email(self, user_email):
            return False
        if not CustomerOperation.validate_mobile(self, user_mobile):
            return False
        if not uo.validate_username(user_name):
            return False
        if not uo.validate_password(user_password):
            return False
        if uo.check_username_exist(user_name):
            return False
        user_id = UserOperation.generate_user_id(self)
        user_password = uo.encryptpassword(user_password)

        user_register_time = time.strftime("%d-%m-%Y %H:%M:%S")

        customer_info = f"{{'user_id': '{user_id}', 'user_name': '{user_name}', 'user_password': '{user_password}', 'user_register_time': '{user_register_time}', 'user_role': 'customer', 'user_email': '{user_email}', 'user_mobile': '{user_mobile}'}}"
        # creates a customer object and appends it to the users.tst file

        with open("data/users.txt", "a", encoding="utf-8") as udata:
            udata.write(customer_info + "\n")
        return True



    # this function is used to get the user info from user.txt file
    def user_info(self):
        data_list = []
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            for line in udata:
                data = line.strip().split(",")
                data_list.append(data)
        return data_list


    def delete_customer(self, customer_id):
        delete = False
        # opens the file in read mode
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            lines = udata.readlines()
            # opens the file in write mode
        with open("data/users.txt", "w", encoding="utf-8") as udata:
            for line in lines:
                cust_info = eval(line.strip())
                # checks if user role is customer id and user id matches to the customer id if it matches if skips that line from writing into the users.txt file
                if cust_info.get('user_role') == 'customer' and cust_info.get('user_id') == customer_id:
                    delete = True
                    continue
                udata.write(line)
        return True

    #this function deletes all the customers from users.txt file by checking the user role
    def delete_all_customer(self):
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            lines = udata.readlines()
        with open("data/users.txt", "w", encoding="utf-8") as udata:
            for line in lines:
                cust_info = eval(line.strip())
                if cust_info.get('user_role') != 'customer':
                    udata.write(line)
        return


    # this function is used to get a list of customers (10 per page)
    def get_customer_list(self, page_number):
        cust_per_page = 10
        cust_list = []
        total_pages = 0

        # open users.txt file in read mode
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            lines = udata.readlines()
            # get the lines if user role is customer and adds it to cust list list
        cust_lines = [eval(line.strip()) for line in lines if "'user_role': 'customer'" in line]
        total_cust = len(cust_lines)
        total_pages = (total_cust + cust_per_page - 1)//cust_per_page

        start_index = (page_number -1) * cust_per_page
        end_index = start_index + cust_per_page

        if start_index >= total_cust:
            return [], page_number, total_cust

        for cust_info in cust_lines[start_index:end_index]:
            customer = Customer(cust_info['user_id'], cust_info['user_name'], cust_info['user_password'],cust_info['user_register_time'], cust_info['user_role'], cust_info['user_email'],cust_info['user_mobile'])
            cust_list.append(customer)

        return cust_list, page_number, total_pages


    def update_profile(self, attribute_name, value, customer_object):
        # this function is used to update the info in customer details
        if not attribute_name or not value or not customer_object:
            return False
        # validate the input values
        cust_dict = eval(str(customer_object))
        if attribute_name == "name":
            if not UserOperation.validate_username(self, value):
                return False
            cust_dict["user_name"] = value
            print(cust_dict["user_name"])
        elif attribute_name == "password":
            if not UserOperation.validate_password(self, value):
                return False
            cust_dict["user_password"] = uo.encryptpassword(value)
        elif attribute_name == "email":
            if not CustomerOperation.validate_email(self, value):
                return False
            cust_dict["user_email"] = value
        elif attribute_name == "mobile":
            if not CustomerOperation.validate_mobile(self, value):
                return False
            cust_dict["user_mobile"] = value
        else:
            return False

        updated_customer_info = str(cust_dict)

        with open("data/users.txt", "r+", encoding="utf-8") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if line.strip() == str(customer_object):
                    file.write(updated_customer_info + "\n")
                else:
                    file.write(line)
            file.truncate()

        return True


    def get_customer_prof(self,user_name,user_password):
        # this function is used to get the details of customer by user name and user password
        user_data = []
        uo = UserOperation()
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            lines = udata.readlines()
        for line in lines:
            user_datalines = eval(line)
            user_data.append(user_datalines)

        for user in user_data:
            if user['user_name'] == user_name and uo.decryptpassword(user['user_password']) == user_password:
                if user['user_role'] == 'customer':
                    return Customer(user['user_id'], user['user_name'], user['user_password'], user['user_register_time'], user['user_role'], user['user_email'], user['user_mobile'])
