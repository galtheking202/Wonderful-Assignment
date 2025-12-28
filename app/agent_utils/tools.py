from logger import Logger
from agent_utils.db import db


# ---------------- TOOLS ---------------- #
def get_client_prescriptions(user_name):
    """
    This function will return the list of prescription medicine for a given user.
    """
    Logger.log("get_client_prescriptions tool called")
    user_name = user_name.strip()
    try:
        user_name = user_name.lower()
    except Exception as e:
        user_name = user_name

    user = db["users"].find_one(
        {
            "$or": [
                {"name_en": {"$regex": f"^{user_name}$", "$options": "i"}},
                {"name_he": {"$regex": f"^{user_name}$", "$options": "i"}}
            ]
        },
        {"_id": 0, "prescription_medicens_id": 1}
    )

    if not user:
        return f"No matching user found for {user_name}."

    pres_ids = user.get("prescription_medicens_id", []) or []
    if not pres_ids:
        return []

    # Query medicens_stock for the prescription ids and return full docs
    meds = list(db["medicens_stock"].find({"id": {"$in": pres_ids}}, {"_id": 0}))
    return meds

def get_medicine_by_name(medicine_name):
    """
    This function will return medicine data by its name 
    """
    Logger.log("get_medicine_by_name tool called")
    medicine_name = medicine_name.strip()
    try:
        medicine_name = medicine_name.lower()
    except Exception as e:
        medicine_name = medicine_name

    meds = list(db["medicens_stock"].find(
        {
            "$or": [
                {"medicine_name_en": {"$regex": f"^{medicine_name}$", "$options": "i"}},
                {"medicine_name_he": {"$regex": f"^{medicine_name}$", "$options": "i"}}
            ]
        },
        {"id": 0, "_id": 0}
    ))
    if len(meds) == 0:
        return f"No matching medicine found for {medicine_name}."
    return meds

def purchase_medicine(user_name: str = "", medicine_name: str = "", amount: int = 1):
    """
    This function processes a medicine purchase for a user.
    it validates user existence, medicine availability, inventory, credits, and prescription requirements.
    If all checks pass, it deducts the inventory and user credits, confirming the purchase.
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
        if medicine.get("id") not in user.get("prescription_medicens_id", []):
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