'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

class Product:
    def __init__(self, pro_id, pro_model, pro_category, pro_name, pro_current_price=0, pro_raw_price=0, pro_discount=0, pro_likes_count =0):
        self.pro_id = pro_id
        self.pro_model = pro_model
        self.pro_category = pro_category
        self.pro_name = pro_name
        self.pro_current_price = pro_current_price
        self.pro_raw_price = pro_raw_price
        self.pro_discount = pro_discount
        self.pro_likes_count = pro_likes_count

    def __str__(self):
        return f"{{'pro_id': '{self.pro_id}', 'pro_model': '{self.pro_model}', 'pro_category': '{self.pro_category}', 'pro_name': '{self.pro_name}', 'pro_current_price': '{self.pro_current_price}', 'pro_raw_price': '{self.pro_raw_price}', 'pro_discount': '{self.pro_discount}', 'pro_likes_count': '{self.pro_likes_count}'}}"

    def save_to_file(self):
        # open the file in append mode
        with open("data/products.txt", "a", encoding="utf-8") as file:
            # append the string to the data in the file
            file.write(str(self) + "\n")
