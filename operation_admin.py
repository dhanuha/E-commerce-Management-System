'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

from operation_user import UserOperation
import time
from model_admin import Admin
class AdminOperation:
    def register_admin(self):
        user_operation = UserOperation()
        # generate unique admin id
        admin_id = user_operation.generate_user_id()
        admin_name = "Dhanu"
        # checks if admin with same name and user id exists
        if self.check_admin_exists(admin_id, admin_name):
            return False
        admin_password = "p12345678"
        # generate current time
        admin_register_time = time.strftime("%d-%m-%Y %H:%M:%S")
        # encrypts the password to save it in the file
        admin_password = user_operation.encryptpassword(admin_password)
        admin = Admin(admin_id, admin_name, admin_password, admin_register_time)

        with open("data/users.txt", "a", encoding="utf-8") as adata:
            adata.write(str(admin) + "\n")

# this function is used to check if the admin with same name and same user id exists
    def check_admin_exists(self, admin_id, admin_name):
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            for line in udata:
                admin_info = eval(line.strip())
                if admin_info['user_id'] == admin_id and admin_info['user_name'] == admin_name:
                    return True
            return False
