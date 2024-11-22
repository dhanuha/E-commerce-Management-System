'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

class Order:
    def __init__(self, order_id, user_id, pro_id, order_time="00-00-0000_00:00:00"):
        self.order_id = order_id
        self.user_id = user_id
        self.pro_id = pro_id
        self.order_time = order_time

    def __str__(self):
        return f"{{'order_id': '{self.order_id}', 'user_id': '{self.user_id}', 'pro_id': '{self.pro_id}', 'order_time': '{self.order_time}'}}"

    def save_to_file(self):
        # open the file in append mode
        with open("data/orders.txt", "a", encoding="utf-8") as file:
            # append the string to the data in the file
            file.write(str(self) + "\n")