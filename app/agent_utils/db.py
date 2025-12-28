from pymongo import MongoClient

mongo_client = MongoClient("mongodb://root:example@localhost:27017/admin")
db = mongo_client["mydb"]