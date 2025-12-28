from logger import Logger
from agent_utils.db import db


# ---------------- TOOLS ---------------- #
def get_medicine_by_id(medicine_id: int = 0):
    """
    This function will return medicine data by its ID.
    """
    Logger.log("get_medicine_by_id tool called")
    return db["medicens_stock"].find_one({"id": medicine_id}, {"_id": 0})

def get_user_by_name(user_name: str = ""):
    """
    This function will return user data by its name (case-insensitive, trims whitespace).
    user data includes: id, name_en, name_he, age, prescription_medicens_id, credits
    """
    Logger.log("get_user_by_name tool called")
    user_name = user_name.strip()
    try:
        user_name = user_name.lower()
    except Exception as e:
        user_name = user_name

    return list(db["users"].find(
        {
            "$or": [
                {"name_en": {"$regex": f"^{user_name}$", "$options": "i"}},
                {"name_he": {"$regex": f"^{user_name}$", "$options": "i"}}
            ]
        },
        {"id": 0, "_id": 0}
    ))

def get_medicine_by_name(medicine_name: str = ""):
    """
    This function will return medicine data by its name (case-insensitive, trims whitespace).
    """
    Logger.log("get_medicine_by_name tool called")
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

def login_user(user_name: str = "", password: str = ""):
    """
    This function will verify user credentials.
    Returns user data if credentials are correct, else returns an error message.
    """
    Logger.log("login_user tool called")
    user_name = user_name.strip()
    password = password.strip()

    user = db["users"].find_one(
        {
            "$or": [
                {"name_en": {"$regex": f"^{user_name}$", "$options": "i"}},
                {"name_he": {"$regex": f"^{user_name}$", "$options": "i"}}
            ],
            "password": password
        },
        {"_id": 0, "password": 0}
    )

    if user:
        return "Login successful. User data: " + str(user)
    else:
        return "Invalid username or password."

def purchase_medicine(user_name: str = "", medicine_name: str = "", amount: int = 1):
    """
    This function processes a medicine purchase for a user.
    It checks if the user has enough credits, if the medicine is in stock,
    and if a prescription is required, verifies the user has it.
    """
    Logger.log("purchase_medicine tool called")
    user_name = user_name.strip().lower()
    medicine_name = medicine_name.strip().lower()

    # Fetch user
    user = db["users"].find_one(
        {
            "$or": [
                {"name_en": {"$regex": f"^{user_name}$", "$options": "i"}},
                {"name_he": {"$regex": f"^{user_name}$", "$options": "i"}}
            ]
        }
    )
    if not user:
        return f"No matching user found for {user_name}."

    # Fetch medicine
    medicine = db["medicens_stock"].find_one(
        {
            "$or": [
                {"medicine_name_en": {"$regex": f"^{medicine_name}$", "$options": "i"}},
                {"medicine_name_he": {"$regex": f"^{medicine_name}$", "$options": "i"}}
            ]
        }
    )
    if not medicine:
        return f"No matching medicine found for {medicine_name}."

    # Check inventory
    if medicine.get("inventory", 0) < amount:
        return f"{medicine_name} is out of stock."

    # Check credits
    if user.get("credits", 0) < medicine.get("credit_cost", 0) * amount:
        return f"{user_name} does not have enough credits to purchase {medicine_name}."

    # Check prescription if required
    if medicine.get("prescription", False):
        # prescription_medicens is a list of medicine ids
        if medicine.get("id") not in user.get("prescription_medicen_id", []):
            return f"{user_name} does not have a prescription for {medicine_name}."

    # Deduct inventory and credits
    db["medicens_stock"].update_one(
        {"_id": medicine["_id"]},
        {"$inc": {"inventory": -1}}
    )
    db["users"].update_one(
        {"_id": user["_id"]},
        {"$inc": {"credits": -medicine.get("credit_cost", 0)}}
    )

    return f"{user_name} successfully purchased {medicine_name}."