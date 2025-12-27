from logger import Logger
import inspect
import json
from openai import OpenAI
from typing import get_type_hints

class BaseAgent:
    def __init__(self,context: str = "",api_key:str=None):
        self.context = context
        self.func_tools_dict = {}
        self.tools = []
        self.client = OpenAI(api_key=api_key)
        self.input_list = []

    def run_agent(self, message: str):
        self.input_list.append({"role": "system", "content": self.context})
        self.input_list.append({"role": "user", "content": message})
        try:
            # 1️⃣ Initial model calls
            response = self.client.responses.create(
                model="gpt-5",
                input=self.input_list,
                tools=self.tools,
            )
            self.input_list += response.output
            print(response.output)
            for item in response.output:
                if item.type == "function_call":
                    print(item)
                    if self.func_tools_dict.get(item.name) is None:
                        raise Exception(f"Tool {item.name} not found")

                    tool = self.func_tools_dict[item.name]
                    arguments = json.loads(item.arguments)

                    # 3️⃣ Execute tool
                    tool_result = tool(**arguments) 

                    self.input_list.append({
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps({
                            item.name: tool_result
                    })
                })
                    
            # 4️⃣ Final model call after tool execution
            response = self.client.responses.create(
                model="gpt-5",
                instructions="Analyze the tool outputs and provide a final response to the user. based on the tool results.",
                tools=self.tools,
                input=self.input_list,
                )
            print(response.output_text) 
            return response.output_text
        except Exception as e:
            Logger.log(f"something went wrong: {e}")
            return None

    def add_tool(self, name: str, func):
        self.tools.append(function_to_tool_schema(func))
        self.func_tools_dict[name] = func


def function_to_tool_schema(func):
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)

    properties = {}
    required = []

    for name, param in sig.parameters.items():
        if param.default is inspect.Parameter.empty:
            required.append(name)

        py_type = type_hints.get(name, str)

        json_type = {
            str: "string",
            int: "number",
            float: "number",
            bool: "boolean",
            list: "array",
            dict: "object"
        }.get(py_type, "string")

        properties[name] = {
            "type": json_type,
            "description": name
        }

    return {
        "type": "function",
        "name": func.__name__,
        "description": func.__doc__ or "",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }