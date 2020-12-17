from pymongo import MongoClient
import psycopg2
import pandas as pd
import os
from sqlalchemy import create_engine
from datetime import datetime


# environment variables
PSQL_PASS = os.environ['PSQL_PASS']
OLAP_USER = "postgres"
OLAP_DB = "olap"
OLAP_HOST = "localhost"
OLTP_USER = "postgres"
OLTP_DB = "oltp"
OLTP_HOST = "localhost"
MONGO_HOST = "localhost"
MONGO_PORT = "27017"


# oltp psql connection
oltp_con = "postgresql+psycopg2://{}:{}@{}:5432/{}".format(OLTP_USER,
                                                           PSQL_PASS,
                                                           OLTP_HOST,
                                                           OLTP_DB)

# mongodb connection
client = MongoClient("mongodb://{}:{}/".format(MONGO_HOST, MONGO_PORT))

# olap psql connection
olap_con = "postgresql+psycopg2://{}:{}@{}:5432/{}".format(OLAP_USER,
                                                           PSQL_PASS,
                                                           OLAP_HOST,
                                                           OLAP_DB)


######### PSQL
oltp = create_engine(oltp_con)
olap = create_engine(olap_con)

# get tables
table_cus = pd.read_sql_table("customers", con=oltp)
table_itm = pd.read_sql_table("items", con=oltp)
table_ord = pd.read_sql_table("orders", con=oltp)

######### MONGO
db = client["transactional"]

# get collections
mongo_cus = pd.DataFrame(db["customers"].find())
mongo_itm = pd.DataFrame(db["items"].find())
mongo_ord = pd.DataFrame(db["orders"].find())

# customers transformations
mongo_cus = mongo_cus.drop(columns=["_id"]).rename(columns={"firstname": "first_name",
                                                            "lastname": "last_name"})

df_cus = table_cus.append(mongo_cus, ignore_index=True)
df_cus = df_cus.drop(columns=["customer_id"])
df_cus["curp"] = df_cus["curp"].fillna("XEXX010101HNEXXXA4")
df_cus = df_cus.assign(id=(df_cus.first_name + df_cus.last_name + df_cus.curp).astype("category").cat.codes)

# items transformations
mongo_itm = mongo_itm.drop(columns=["_id"]).rename(columns={"title": "item_name",
                                                            "price": "item_price"})

df_itm = table_itm.append(mongo_itm, ignore_index=True)
df_itm = df_itm.drop(columns=["item_id"])
df_itm = df_itm.assign(id=(df_itm.item_name).astype("category").cat.codes)

# orders transformations
ord_items = pd.json_normalize(mongo_ord["items"])
ord_cust = pd.json_normalize(mongo_ord["customer"])
mongo_ord = mongo_ord.join(ord_items)
mongo_ord = mongo_ord.join(ord_cust)
mongo_ord['date'] = mongo_ord['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
mongo_ord = mongo_ord.drop(columns=["_id", "customer", "items", "timestamp"])
mongo_ord = mongo_ord.rename(columns={"title": "item_name", "price": "item_price",
                                      "quantity": "item_quantity", "firstname": "first_name",
                                      "lastname": "last_name"})


df_ord = pd.merge(table_ord, table_cus, on="customer_id")
df_ord = pd.merge(df_ord, table_itm, on="item_id")
df_ord = df_ord.drop(columns=['order_id', "customer_id", "item_id", "curp", "rfc"])
df_ord = df_ord.rename(columns={"price": "total"})
df_ord = df_ord.append(mongo_ord, ignore_index=True)
df_ord = df_ord.assign(id=(df_ord.date).astype("category").cat.codes)

# insert to sql
df_cus.to_sql("customers",
              con=olap,
              index=False,
              if_exists="append")
print("Customers done.")

df_itm.to_sql("items",
              con=olap,
              index=False,
              if_exists="append")
print("Items done.")

df_ord.to_sql("orders",
              con=olap,
              index=False,
              if_exists="append")
print("Orders done.")
