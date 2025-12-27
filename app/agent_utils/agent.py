from xmlrpc import client
from contexts import AGENT_CONTEXT
from dotenv import load_dotenv
from .tools import *
from openai import OpenAI
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
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.input_list = []
    def invoke_openai_with_tools(self,message: str,tools: list = TOOLS):
        self.input_list.append({"role": "system", "content": self.context})
        self.input_list.append({"role": "user", "content": message})
        try:
            # 1️⃣ Initial model calls
            response = self.client.responses.create(
                model="gpt-5",
                input=self.input_list,
                tools=tools,
            )
            self.input_list += response.output

            for item in response.output:
                if item.type == "function_call":
                    print(item)
                    if FUNC_TOOLS.get(item.name) is None:
                        raise Exception(f"Tool {item.name} not found")
                    
                    tool = FUNC_TOOLS[item.name]
                    arguments = json.loads(item.arguments)

                    # 3️⃣ Execute tool
                    tool_result = tool(**arguments) 

                    self.input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({
                        item.name : tool_result
                    })
                })
                    
            print(self.input_list)
            # 4️⃣ Final model call after tool execution
            response = self.client.responses.create(
                model="gpt-5",
                instructions="Analyze the tool outputs and provide a final response to the user. based on the tool results only.",
                tools=tools,
                input=self.input_list,
                )
            return response.output_text
        except Exception as e:
            Logger.log(f"something went wrong: {e}")
            return None

