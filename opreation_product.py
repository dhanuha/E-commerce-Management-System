'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

import pandas as pd
from model_product import Product
import os
import matplotlib.pyplot as plt

class ProductOperation:
    def extract_products_from_files(self):
        # gets all the product details from csv file and adds it into products.txt file
        directory = "data/product"
        csv_files = [os.path.join(directory ,file) for file in os.listdir(directory) if file.endswith('.csv')]

        # these are the required columns it only gets the data from these columns
        necessary_col = ['id', 'model', 'category', 'name', 'current_price', 'raw_price', 'discount', 'likes_count']
        req_col = ['pro_id', 'pro_model', 'pro_category', 'pro_name', 'pro_current_price', 'pro_raw_price', 'pro_discount', 'pro_likes_count']

        for file in csv_files:
            df = pd.read_csv(file)
            final_col = df[necessary_col].rename(columns=dict(zip(necessary_col,req_col)) )
            for index, row in final_col.iterrows():
                data_line = str(row.to_dict())

                with open("data/products.txt", "a", encoding="utf-8") as udata:
                    udata.write(data_line + '\n')



    def get_product_list(self,page_number):
        # gets the product list by page number (10 products per page)
        prod_per_page = 10
        prod_list = []
        total_pages = 0

        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()
        prod_lines = [eval(line.strip()) for line in lines ]
        total_prod = len(prod_lines)
        total_pages = (total_prod + prod_per_page - 1)//prod_per_page

        start_index = (page_number -1) * prod_per_page
        end_index = start_index + prod_per_page

        if start_index >= total_prod:
            return [], page_number, total_prod

        for prod_info in prod_lines[start_index:end_index]:
            product = Product(prod_info['pro_id'], prod_info['pro_model'], prod_info['pro_category'], prod_info['pro_name'], prod_info['pro_current_price'], prod_info['pro_raw_price'], prod_info['pro_discount'], prod_info['pro_likes_count'])
            prod_list.append(product)

        return prod_list, page_number, total_pages


    def delete_product(self, product_id):
        # deletes the product using product id
        delete = False
        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()
        with open("data/products.txt", "w", encoding="utf-8") as pdata:
            for line in lines:
                prod_info = eval(line.strip())
                # checks if product id matches and if it matches skips it from writing it to the file
                if prod_info.get('pro_id') == product_id:
                    delete = True
                    continue
                pdata.write(line)
        return delete

    def get_product_list_by_keyword(self, keyword):
        # gets the list of products if the keyword is present in the product name
        prod_list = []

        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()
            prod_lines = [eval(line.strip()) for line in lines]

            for prod_info in prod_lines:
                if keyword.lower() in prod_info['pro_name'].lower():
                    product = Product(prod_info['pro_id'], prod_info['pro_model'], prod_info['pro_category'],prod_info['pro_name'], prod_info['pro_current_price'], prod_info['pro_raw_price'],prod_info['pro_discount'],prod_info['pro_likes_count'])
                    prod_list.append(product)

            return prod_list

    def get_product_by_id(self, product_id):
        # gets the product details by using product id
        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()
            prod_lines = [eval(line.strip()) for line in lines]

            for prod_info in prod_lines:
                if prod_info.get('pro_id') == product_id:
                    product = Product(prod_info['pro_id'], prod_info['pro_model'], prod_info['pro_category'],prod_info['pro_name'], prod_info['pro_current_price'], prod_info['pro_raw_price'],prod_info['pro_discount'], prod_info['pro_likes_count'])
                    return product
        return None

    def delete_all_product(self):
        # deletes all the products from the products.txt file
        with open("data/products.txt", "w", encoding="utf-8") as pdata:
            pdata.truncate()


    def get_product_price(self, product_id):
        # gets the price of product using product id
        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()
            prod_lines = [eval(line.strip()) for line in lines]

            for prod_info in prod_lines:
                if prod_info.get('pro_id') == product_id:
                    return prod_info.get('pro_current_price')
        return None

    def generate_category_figure(self):
        # generates the graph based on the number of products in each category
        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()

        count = {}

        for line in lines:
            prod_info = eval(line.strip())
            category = prod_info['pro_category']
            if category in count:
                count[category] += 1
            else:
                count[category] = 1

        ordered_cat = sorted(count.items(), key=lambda x: x[1], reverse=True)
        categories , product_counts = zip(*ordered_cat)

        plt.bar(categories,product_counts)

        plt.xlabel("category")
        plt.ylabel("product_count")
        plt.title("num of products in each Category")
        plt.xticks(rotation=90)

        path = "data/figure/category_figure1.png"
        os.makedirs(os.path.dirname(path), exist_ok= True)
        plt.savefig(path)
        plt.close()

    def generate_discount_figure(self):
        # gets the products piechart based on their discount ranges
        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()

        d_count = [0, 0, 0]

        for line in lines:
            prod_info = eval(line.strip())
            discount = prod_info['pro_discount']

            if discount < 30:
                d_count[0] += 1
            elif discount >= 30 and discount < 60:
                d_count[1] += 1
            else:
                d_count[2] += 1
        # assigning the labels and colours
        labels = ['<30%', '30%-60%', '>60%']
        colours = ['#2196F3', '#9E9E9E', '#9C27B0']

        plt.pie(d_count, labels = labels ,colors = colours, autopct= '%1.1f%%' , startangle=90)
        plt.axis('equal')
        plt.title("Percentage of Products by Discount Range")
        path = "data/figure/discount_figure1.png"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # saves it to the figure directory
        plt.savefig(path)
        plt.close()

    def generate_likes_count_figure(self):
        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()

        l_count = {}

        for line in lines:
            prod_info = eval(line.strip())
            category = prod_info['pro_category']
            likes = prod_info['pro_likes_count']

            if category in l_count:
                l_count[category] += likes
            else:
                l_count[category] = likes

        ordered_lcount = sorted(l_count.items(), key=lambda x: x[1])

        categories, counts = zip(*ordered_lcount)

        # plt.figure(figsize=(10, 6))

        plt.bar(categories, counts)
        plt.xlabel('Sum of Likes Count')
        plt.ylabel('Category')
        plt.title('Sum of Products Likes Count by Category')
        plt.xticks(rotation=90)

        path = 'data/figure/likes_count_figure.png'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # saves it to the figure directory
        plt.savefig(path)
        plt.close()


    def generate_discount_likes_count_figure(self):
        # generates a scatter graph btw the relation of discount and likes count
        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            lines = pdata.readlines()
        l_count = []
        discounts = []
        for line in lines:
            prod_info = eval(line.strip())
            likes = prod_info['pro_likes_count']
            discount = prod_info['pro_discount']
            l_count.append(likes)
            discounts.append(discount)

        plt.figure(figsize=(8,8))
        plt.scatter(discounts, l_count, color='#2196F3', alpha = 0.5)
        plt.xlabel('Discount')
        plt.ylabel('LikesCount')
        plt.title('Discount and LikesCount Relationship')

        path = 'data/figure/discount_likes_count_figure.png'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # saves it to the figure directory
        plt.savefig(path)
        plt.close()
