from contexts import AGENT_CONTEXT
from dotenv import load_dotenv
from .tools import *
import json


FUNC_TOOLS = {"get_medicine_data_by_name":get_medicine_data_by_name}

import requests
import os

load_dotenv()

API_URL = "https://api.openai.com/v1/responses"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class MedicineAsisstentAgent:
    def __init__(self):
        self.context = AGENT_CONTEXT
    def run_agent(self, msg: str):
        response = agent_request(self.context,msg,OPENAI_API_KEY)
        tool_input = []
        for output in response["output"]:
            if output["type"] == "function_call":
                tool = FUNC_TOOLS[output["name"]]
                data = tool("Amoxicillin") # change it
                print(output)
                tool_input.append({"role":"tool","tool_call_id":output["call_id"],"content":str(data)})
        if len(tool_input) > 0:
            return tool_preformed(response["id"],tool_input,OPENAI_API_KEY)
                
        


{'model': 'gpt-5', 'previous_response_id': 'resp_074dd57058b07efc01694f3194eb348196aabb275954d2f6c3', 'input': [{'role': 'tool', 'tool_call_id': 'call_g0CliuRmE7FWw2sM2h8s4l06', 'content': [{'medicine_id': 1, 'medicine_name': 'Amoxicillin', 'prescription': True}]}]}     

