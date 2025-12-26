import requests
import json
from contexts import AGENT_CONTEXT

# ---------------- TOOLS ---------------- #



def get_medicine_data_by_name(medicine_name)
    # retrive medicine data by medicine_name
    # if medicine name does not exist return None
    return
    
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": get_medicine_data_by_name.__name__,
            "description": get_medicine_data_by_name.__docs__,
            "parameters": {
                "type": "string",
                "required": ["medicine_name"]
            }
        }
    },
]

class MedicineAsisstentAgent:
    def init():
        self.context = AGENT_CONTEXT
    def invoke():
        
    


