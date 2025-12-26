import requests
import json
from contexts import AGENT_CONTEXT
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from logger import Logger

load_dotenv()

API_URL = "https://api.openai.com/v1/responses"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------- TOOLS ---------------- #

client = MongoClient("mongodb://root:example@mongo:27017")
db = client["mydb"]

#   


def get_medicine_data_by_name(medicine_name):
    ### this function will return medicine data by its name, data will include availability prescription requierment###
    Logger.log("get_medicine_data_by_name tool called")
    return db["medicens_stock"].find({"medicine_name":medicine_name})

TOOLS = [
   {
    "type": "function",
    "name": get_medicine_data_by_name.__name__,
    "description": get_medicine_data_by_name.__doc__,
    "parameters": {
        "type": "object",
        "properties": {
            "medicine_name": {
                "type": "string",
                "description": "Name of the medicine"
            }
        },
        "required": ["medicine_name"]
    }
}
]
class MedicineAsisstentAgent:
    def __init__(self):
        self.context = AGENT_CONTEXT
        get_medicine_data_by_name("Amoxicillin")
    def invoke(self, message: str):
        payload = {
            "model": "gpt-5",
            "input": [
                {
                    "role": "system",
                    "content": str(self.context)
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "tools": TOOLS
        }

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.openai.com/v1/responses",
            headers=headers,
            json=payload,
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        response.raise_for_status()
        return response.json()



