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

def deduct_medicine_inventory(medicine_name: str = "", amount: int = 0):
    """
    This function will deduct the inventory of a medicine by its name used when client purchase medicine.
    """
    Logger.log("deduct_medicine_inventory tool called")
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
    
def deduct_user_credits(user_name: str = "", amount: int = 0):
        """
        This function will deduct the credits of a user by their name used when client purchase medicine.
        """
        Logger.log("deduct_user_credits tool called")
        user_name = user_name.strip()

        try:
            user_name = user_name.lower()
        except Exception as e:
            user_name = user_name

        result = db["users"].update_one(
            {
                "$or": [
                    {"name_en": {"$regex": f"^{user_name}$", "$options": "i"}},
                    {"name_he": {"$regex": f"^{user_name}$", "$options": "i"}}
                ]
            },
            {
                "$inc": {"credits": -amount}
            }
        )

        if result.modified_count > 0:
            return f"Deducted {amount} credits from {user_name}."
        else:
            return f"No matching user found for {user_name}."
        



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
        },
    },
    {
        "type": "function",
        "name": deduct_medicine_inventory.__name__,
        "description": deduct_medicine_inventory.__doc__,
        "parameters": {
            "type": "object",
            "properties": {
                "medicine_name": {
                    "type": "string",
                    "description": "Name of the medicine"
                },
                "amount": {
                    "type": "integer",
                    "description": "Amount to deduct from inventory"
                }
            },
            "required": ["medicine_name", "amount"]
        },
    },
    {
        "type": "function",
        "name": deduct_user_credits.__name__,
        "description": deduct_user_credits.__doc__,
        "parameters": {
            "type": "object",
            "properties": {
                "user_name": {
                    "type": "string",
                    "description": "Name of the user"
                },
                "amount": {
                    "type": "integer",
                    "description": "Amount of credits to deduct"
                }
            },
            "required": ["user_name", "amount"]
        },
    }
]