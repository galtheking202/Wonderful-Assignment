from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
if os.getenv("RUN_ENV") == "docker":
    CONNECTION_STRING = "mongodb://root:example@mongo:27017" # Docker setup
else:
    CONNECTION_STRING = "mongodb://root:example@localhost:27017/admin" # Local setup

mongo_client = MongoClient(CONNECTION_STRING)
db = mongo_client["mydb"]