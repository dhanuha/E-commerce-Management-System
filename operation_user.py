'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

import random
import re
from model_customer import Customer
from model_admin import Admin
class UserOperation:
    def generate_user_id(self):
        # generate a random 10 digit user id
        user_id = random.randint(1000000000, 9999999999)
        while True:
            # checks if the user_id exists
            for line in self.user_info():
                if str(user_id) == line[0].strip():
                    # generate another new user id if user id exists
                    user_id = random.randint(1000000000, 9999999999)
                    break
            return "u_"+str(user_id)

    def generate_randomstr(self, length):
        charc = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        # generates a random string of given length
        return ''.join(random.choice(charc) for _ in range(length))
    def encryptpassword(self,user_password):
        # generate a random string with length double the length of user password
        random_str = self.generate_randomstr(len(user_password) * 2)
        encryptedpassword = ''
        for i in range(len(user_password)):
            # encrypt the password in a way that inserts the user password character after every two random string characters
            encryptedpassword += random_str[2 * i] + random_str[2 * i + 1] + user_password[i]
            # add markers at the start and end of encrypted password
        encryptedpassword = "^^" + encryptedpassword + "$$"
        return encryptedpassword

    def decryptpassword(self, encryptedpassword):
        # removes the markers of the encrypted password
        encryptedpassword = encryptedpassword[2:-2]
        decryptedpassword = ""
        # decrypts the password by taking 3rd character from the start
        for i in range(len(encryptedpassword)):
            if (i + 1) % 3 == 0:
                decryptedpassword += encryptedpassword[i]

        return decryptedpassword

    def check_username_exist(self, user_name):
        # opens the file in read mode
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            lines = udata.readlines()
            for line in lines:
                # extract username from the line
                match = re.search(r"'user_name': '([^']+)'", line)
                # checks if username matches to the existing usernames
                if user_name == match.group(1):
                    # returns true if exists
                    return True
            else:
                # returns false if it doesnt exist
                return False

    def validate_username(self, user_name):
        # checks if len of username is atleast 5 characters
        if len(user_name) < 5:
            return False
        for i in user_name:
            # checks if the username is only alphabets and underscore
            if not (i.isalpha() or i == '_'):
                return False
        else:
            return True




    def validate_password(self, user_password):
        # checks if len of username is atleast 5 characters
        if len(user_password) < 5:
            return False
        hasletter = False
        hasnum = False
        # checks it has both alphabets and numbers in user password
        for i in user_password:
            if i.isalpha():
                hasletter = True
            elif i.isdigit():
                hasnum = True
        return hasletter and hasnum


    def login(self, user_name, user_password):
        user_data = []
        # open the file in read mode
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            lines = udata.readlines()
        for line in lines:
            user_datalines = eval(line)
            user_data.append(user_datalines)

        for user in user_data:
            # checks if username and user password matches
            if user['user_name'] == user_name and self.decryptpassword(user['user_password']) == user_password:
                # checks the user role
                if user['user_role'] == 'customer':
                    # returns customer object if user role is customer
                    return Customer(self, user_name, user_password)
                elif user['user_role'] == 'admin':
                    # returns admin object if user role is admin
                    return Admin(self, user_name, user_password)
        return None



# this function is used to get the data from uers.txt files
    def user_info(self):
        data_list = []
        with open("data/users.txt", "r", encoding="utf-8") as udata:
            for line in udata:
                data = line.strip().split(",")
                data_list.append(data)
        return data_list

