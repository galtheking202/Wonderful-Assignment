
from pymongo import MongoClient
from logger import Logger
import requests

# ---------------- TOOLS ---------------- #
client = MongoClient("mongodb://root:example@mongo:27017")
db = client["mydb"]


def agent_request(context:str,message:str,api_key:str):
    payload = {
            "model": "gpt-5",
            "input": [
                {
                    "role": "system",
                    "content": str(context)
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            "tools": TOOLS
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers=headers,
        json=payload,
        timeout=30
    )
    if response.status_code != 200:
        Logger.log(f"something went wrong {response.status_code}")
    else:
        return response.json()
    

def tool_preformed(previous_response_id,tool_input,api_key):
    payload = {
        "model": "gpt-5",
        "previous_response_id": previous_response_id,
        "input": tool_input
    }

    print(payload)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers=headers,
        json=payload,
        timeout=30
    )
    if response.status_code != 200:
        Logger.log(f"something went wrong second tool {response.reason}")
    else:
        return response.json()
    


def get_medicine_data_by_name(medicine_name):
    ### this function will return medicine data by its name, data will include availability prescription requierment###
    Logger.log("get_medicine_data_by_name tool called")
    return list(db["medicens_stock"].find({"medicine_name":medicine_name},{"id":0,"_id":0}))


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