'''
Assignment3

Dhanunjai Sai Kumar Andey
student id : 33575630

Date created: 30/05/2023
Date last modified: 14/06/2023
'''

import time
import random
from model_order import Order
from operation_user import UserOperation
from opreation_product import ProductOperation
import matplotlib.pyplot as plt
import numpy as np

class OrderOperation:
    def generate_order_id(self):
        # generate unique order id
        order_id = random.randint(10000, 99999)
        while True:
            for line in self.order_info():
                if str(order_id) == line[0].strip():
                    # checks if order id exists, if it exists it generates again another new order id
                    order_id = random.randint(10000, 99999)
                    break
            return "o_"+str(order_id)

    def create_an_order(self, customer_id, product_id, create_time = None):
        # this function is used to create an order by taking customer id, product id and create time
        if not create_time:
            # generate current time
            create_time = time.strftime("%d-%m-%Y %H:%M:%S")
        order_id = OrderOperation.generate_order_id(self)
        order_info = f"{{'order_id': '{order_id}', 'user_id': '{customer_id}', 'pro_id': '{product_id}', 'order_time': '{create_time}'}}"
        with open("data/orders.txt", "a", encoding="utf-8") as odata:
            odata.write(order_info + "\n")
        return True

    def delete_order(self,order_id):
        # deletes an order by order id
        delete = False
        with open("data/orders.txt", "r", encoding="utf-8") as odata:
            lines = odata.readlines()
        with open("data/orders.txt", "w", encoding="utf-8") as odata:
            for line in lines:
                order_info = eval(line.strip())
                # checks if order id matches
                if order_info.get('order_id') == order_id:
                    delete = True
                    continue
                odata.write(line)
        return True

    def get_order_list(self, customer_id, page_number):
        # gets the list of orders of a customer by customer id
        orders_per_page = 10
        order_list = []
        total_pages = 0

        with open("data/orders.txt", "r", encoding="utf-8") as odata:
            lines = odata.readlines()
        order_lines = [eval(line.strip()) for line in lines if eval(line.strip()).get('user_id') == customer_id]
        total_orders = len(order_lines)
        total_pages = (total_orders + orders_per_page - 1) // orders_per_page

        start_index = (page_number - 1) * orders_per_page
        end_index = start_index + orders_per_page

        if start_index >= total_orders:
            return [], page_number, total_orders

        for order_info in order_lines[start_index:end_index]:
            order = Order(order_info['order_id'], order_info['user_id'], order_info['pro_id'],order_info['order_time'])
            order_list.append(order)

        return order_list, page_number, total_pages


    def generate_test_order_data(self):
        # generates test data for 10 customers with orders of 50-200
        cust_ids = []
        for i in range(10):
            UP = UserOperation()
            cust_id = UP.generate_user_id()
            cust_ids.append(cust_id)
        for cust_id in cust_ids:
            num_orders = random.randint(50,200)

            for o in range(num_orders):
                prod_ids = []
                with open("data/products.txt", "r", encoding="utf-8") as pdata:
                    lines = pdata.readlines()
                    for line in lines:
                        prod_info = eval(line.strip())
                        prod_id = prod_info.get('pro_id')
                        prod_ids.append(prod_id)

                prod_id = random.choice(prod_ids)

                day = random.randint(1 , 28)
                month = random.randint(1, 12)
                hour = random.randint(0, 23)
                min = random.randint(0, 59)
                sec = random.randint(0, 59)
                order_time = f"{day:02d}-{month:02d}-{time.strftime('%Y')} {hour:02d}:{min:02d}:{sec:02d}"

                order_id = OrderOperation.generate_order_id(self)
                order_info = f"{{'order_id': '{order_id}', 'user_id': '{cust_id}', 'pro_id': '{prod_id}', 'order_time': '{order_time}'}}"

                # appends the data to the orders.txt file
                with open("data/orders.txt", "a", encoding="utf-8") as odata:
                    odata.write(order_info + "\n")

    def generate_single_customer_consumption_figure(self, customer_id):
        # generate a consumption figure for a customer by customer id by importing matplotlib
        monthly_consumption = {}
        order_data = OrderOperation.order_info(self)
        product_operation = ProductOperation()

        # it takes the history of orders of that customer
        cust_orders = [order for order in order_data if eval(order[1].strip().split(":")[1].strip()) == customer_id]


        for order in cust_orders:
            order_month = int(order[3].split('-')[1].strip().lstrip('0'))
            product_id = int(eval(order[2].strip().split(":")[1].strip()))
            order_price = product_operation.get_product_price(product_id)
            # gets the price of product
            if order_price is not None:
                if order_month in monthly_consumption:
                    # adds the price of orders based on months
                    monthly_consumption[order_month] += float(order_price)
                else:
                    monthly_consumption[order_month] = float(order_price)
        months = list(range(1, 13))
        consumption_values = [float(monthly_consumption.get(month, 0)) for month in months]

        months = [str(month) for month in months]
        plt.bar(months, consumption_values)
        plt.xlabel("month")
        plt.ylabel("consumption")
        plt.title(f"Monthly Consumption by {customer_id}")
        plt.ylim(0, max(consumption_values) + 10)
        plt.yticks(np.arange(0, max(consumption_values) + 10, 10))
        plt.show()
        # shows the graph based of the monthly consumption of the customer

    def generate_all_customer_consumption_figure(self):
        # generate a consumption figure for all customer by importing matplotlib
        monthly_consumption = {}
        order_data = OrderOperation.order_info(self)
        order_operation = ProductOperation()

        all_orders = [order for order in order_data]
        # gets all the order details

        for order in all_orders:
            order_month = int(order[3].split('-')[1].strip().lstrip('0'))
            product_id = int(eval(order[2].strip().split(":")[1].strip()))
            order_price = order_operation.get_product_price(product_id)
            if order_price is not None:
                if order_month in monthly_consumption:
                    # adds the price of orders based on months
                    monthly_consumption[order_month] += float(order_price)
                else:
                    monthly_consumption[order_month] = float(order_price)
        months = list(range(1, 13))
        consumption_values = [float(monthly_consumption.get(month, 0)) for month in months]

        months = [str(month) for month in months]
        plt.bar(months, consumption_values)
        plt.xlabel("month")
        plt.ylabel("consumption")
        plt.title(f"Monthly Consumption by all customers")
        plt.ylim(0, max(consumption_values) + 10)
        plt.yticks(np.arange(0, max(consumption_values) + 10, 10))
        plt.show()
        # shows the graph based of the monthly consumption of all the customers

    def generate_all_top_10_best_sellers_figure(self):
        # this function generates a graph of top 10 best sellers by taking likes  count as reference
        prod_likes = {}

        with open("data/products.txt", "r", encoding="utf-8") as pdata:
            prod_info = [eval(line.strip()) for line in pdata]

        for product in prod_info:
            prod_id = product.get('pro_id')
            prod_likes[prod_id] = product.get('pro_likes_count', 0)
            # gets product id and nuber of likes of that product

        sorted_list = sorted(prod_likes.items(), key = lambda x: x[1], reverse = True )
        top_10 = sorted_list[:10]
        prod_names = []
        likes_count = []

        for prod_id , likes in top_10:
            for product in prod_info:
                if product.get('pro_id') == prod_id:
                    prod_names.append(product.get('pro_name'))
                    # gets the name of product based on product id
                    likes_count.append(likes)
                    break


        plt.bar(prod_names , likes_count)
        plt.xlabel("PRODUCT")
        plt.ylabel("LIKES")
        plt.title(" Top 10 best selling products ")
        plt.xticks(rotation = 90)
        plt.xticks(fontsize = 6)
        plt.show()
        # shows the graph of top 10 best seller



    def delete_all_orders(self):
        # deletes all the orders in orders.txt file
        with open("data/orders.txt", "w", encoding="utf-8") as odata:
            odata.truncate()


    def get_all_order_list(self,page_number):
        # gets the order list by page number (10 orders per page)
        order_per_page = 10
        order_list = []
        total_pages = 0

        with open("data/orders.txt", "r", encoding="utf-8") as odata:
            lines = odata.readlines()
        order_lines = [eval(line.strip()) for line in lines ]
        total_orders = len(order_lines)
        total_pages = (total_orders + order_per_page - 1)//order_per_page

        start_index = (page_number -1) * order_per_page
        end_index = start_index + order_per_page

        if start_index >= total_orders:
            return [], page_number, total_orders

        for order_info in order_lines[start_index:end_index]:
            order = Order(order_info['order_id'], order_info['user_id'], order_info['pro_id'], order_info['order_time'])
            order_list.append(order)

        return order_list, page_number, total_pages



    def order_info(self):
        # gets the order info from orders.txt file
        data_list = []
        with open("data/orders.txt", "r", encoding="utf-8") as odata:
            for line in odata:
                data = line.strip().split(",")
                data_list.append(data)
        return data_list
