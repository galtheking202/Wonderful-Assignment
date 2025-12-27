from pymongo import MongoClient
from logger import Logger
import requests

# ---------------- TOOLS ---------------- #
mongo_client = MongoClient("mongodb://root:example@mongo:27017")
db = mongo_client["mydb"]

def get_medicine_data_by_name(medicine_name: str = ""):
    """
    This function will return medicine data by its name (case-insensitive, trims whitespace).
    """
    Logger.log("get_medicine_data_by_name tool called")
    medicine_name = medicine_name.strip()

    try:
        medicine_name = medicine_name.lower()
    except Exception as e:
        medicine_name = medicine_name

    return list(db["medicens_stock"].find(
        {
            "$or": [
                {"medicine_name_en": {"$regex": f"^{medicine_name}$", "$options": "i"}},
                {"medicine_name_he": {"$regex": f"^{medicine_name}$", "$options": "i"}}
            ]
        },
        {"id": 0, "_id": 0}
    ))

def dedact_medicine_inventory(medicine_name: str = "", amount: int = 0):
    """
    This function will deduct the inventory of a medicine by its name.
    """
    Logger.log("dedact_medicine_inventory tool called")
    medicine_name = medicine_name.strip()

    try:
        medicine_name = medicine_name.lower()
    except Exception as e:
        medicine_name = medicine_name

    result = db["medicens_stock"].update_one(
        {
            "$or": [
                {"medicine_name_en": {"$regex": f"^{medicine_name}$", "$options": "i"}},
                {"medicine_name_he": {"$regex": f"^{medicine_name}$", "$options": "i"}}
            ]
        },
        {
            "$inc": {"inventory": -amount}
        }
    )

    if result.modified_count > 0:
        return f"Deducted {amount} from {medicine_name} inventory."
    else:
        return f"No matching medicine found for {medicine_name}."

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