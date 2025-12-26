from pymongo import MongoClient

client = MongoClient("mongodb://root:example@mongo:27017")
db = client["mydb"]

print(list(db.users.find()))
print(list(db.medicens_stoc.find()))

print("hello world")