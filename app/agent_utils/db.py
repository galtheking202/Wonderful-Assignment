from pymongo import MongoClient

mongo_client = MongoClient("mongodb://root:example@mongo:27017")
db = mongo_client["mydb"]