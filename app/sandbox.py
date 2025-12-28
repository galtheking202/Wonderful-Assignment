from pymongo import MongoClient
import time

for i in range(10):
    try:
        client = MongoClient("mongodb://root:example@localhost:27017/admin")
        print("Databases:", client.list_database_names())
        print(client["mydb"].list_collection_names())
        break
    except Exception as e:
        print("Waiting for MongoDB...", e)
        time.sleep(2)
