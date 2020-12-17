from pymongo import MongoClient


# data to be stored
customers_data = [{"firstname": "Bob", "lastname": "Adams"},
                  {"firstname": "Amy", "lastname": "Smith"},
                  {"firstname": "Rob", "lastname": "Bennet"}]

items_data = [{"title": "USB", "price": 10.2},
              {"title": "Mouse", "price": 12.23},
              {"title": "Monitor", "price": 199.99}]

orders_data = [{"timestamp": 1608091200,
               "address": "20 W 34th St, New York, NY 10001",
               "customer": {"firstname": "Bob", "lastname": "Adams"},
               "items": {"title": "Mouse", "price": 12.23, "quantity": 1},
               "total": 12.23,
               "comments": "Please send before Christmas."},
              {"timestamp": 1608092100,
               "address": "20 W 34th St, New York, NY 10001",
               "customer": {"firstname": "Bob", "lastname": "Adams"},
               "items": {"title": "USB", "price": 10.2, "quantity": 1},
               "total": 10.2,
               "comments": "Please, add this order to my previous order, send before Christmas, please."},
              {"timestamp": 1608084000,
               "address": "90 Bedford St, New York, NY 10014",
               "customer": {"firstname": "Rob", "lastname": "Bennet"},
               "items": {"title": "Monitor", "price": 199.99, "quantity": 1},
               "total": 199.99}]

# connect to mongo
client = MongoClient("mongodb://localhost:27017/")
db = client["transactional"]

# insert values to mongodb
cust = db["customers"]
cust.insert_many(customers_data)

items = db["items"]
items.insert_many(items_data)

orders = db["orders"]
orders.insert_many(orders_data)
