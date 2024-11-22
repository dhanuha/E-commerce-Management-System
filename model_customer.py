'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

from model_user import User


class Customer(User):
    def __init__(self, user_id, user_name, user_password, user_register_time="00-00-0000_00:00:00",
                 user_role="customer", user_email="", user_mobile=""):
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)
        self.user_email = user_email
        self.user_mobile = user_mobile

    def __str__(self):
        return f"{{'user_id': '{self.user_id}', 'user_name': '{self.user_name}', 'user_password': '{self.user_password}', 'user_register_time': '{self.user_register_time}', 'user_role': '{self.user_role}', 'user_email': '{self.user_email}', 'user_mobile': '{self.user_mobile}'}}"

    def save_to_file(self):
        # open the file in append mode
        with open("data/users.txt", "a", encoding="utf-8") as file:
            # checks if the user role is customer
            if self.user_role == "customer":
                # append the string to the data in the file
                file.write(str(self) + "\n")
