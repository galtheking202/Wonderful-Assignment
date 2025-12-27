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
    def invoke_openai_with_tools(self,message: str,tools: list = TOOLS):
        try:
            # 1️⃣ Initial model calls
            response = self.client.responses.create(
                model="gpt-5",
                input=[
                    {"role": "system", "content": self.context},
                    {"role": "user", "content": message},
                ],
                tools=tools,
            )

            # 2️⃣ Check if model wants to call a tool
            tool_calls = response.output
            tool_outputs = []

            for item in tool_calls:
                if item.type == "function_call":
                    tool_name = item.name
                    arguments = json.loads(item.arguments)
                    print(type(arguments))
                    if FUNC_TOOLS.get(tool_name,None) is None:
                        raise ValueError(f"Tool {tool_name} not implemented")

                    tool = FUNC_TOOLS[tool_name]
                    # 3️⃣ Execute tool
                    tool_result = tool(**arguments)

                    tool_outputs.append({
                        "type": "tool_output",
                        "tool_call_id": item.id,
                        "output": tool_result
                    })

            # 4️⃣ If no tools were called, return model output
            if not tool_outputs:
                return response.output_text

            # 5️⃣ Send tool results back to model
            final_response = client.responses.create(
                model="gpt-5",
                input=tool_outputs,
            )

            return final_response.output_text

        except Exception as e:
            Logger.log(f"something went wrong: {e}")
            return None
        
