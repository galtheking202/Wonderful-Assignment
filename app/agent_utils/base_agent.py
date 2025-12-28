from logger import Logger
import inspect
import json
from openai import OpenAI
from typing import get_type_hints

class BaseAgent:
    """Lightweight agent wrapper for the OpenAI Responses API.

    This class simplifies building multi-step agent interactions with an
    `OpenAI` responses client by:
    - managing a persistent conversation `input_list` (system, user, and
      function-call outputs),
    - registering Python callables as model-invokable tools (exposing a
      JSON-schema for the model),
    - executing tool calls returned by the model and feeding results back
      into subsequent model calls,
    - supporting streaming and non-streaming flows.

    Attributes:
        context (str): System-level context or instructions provided to the model.
        func_tools_dict (dict): Mapping from tool name to Python callable.
        tools (list): List of tool schemas (JSON) passed to the model.
        client (OpenAI): Client instance used to call the Responses API.
        input_list (list): Accumulated conversation messages and tool outputs
            across the multi-step interaction.

    Methods:
        run_agent_stream(message): Perform a streaming agent interaction that
            yields text deltas while optionally executing tools called by the model.
        run_agent(message): Perform a synchronous (non-streaming) agent
            interaction and return the final response text.
        add_tool(name, func): Register a Python function as a callable tool
            available to the model.

    Usage example:
        agent = BaseAgent(context='You are a helpful assistant', api_key='sk-...')
        agent.add_tool('my_tool', my_tool_function)
        result = agent.run_agent('Use my_tool to fetch data')
    """
    def __init__(self,context: str = "",tool_instructions: str = "",api_key:str=None):
        self.context = context
        self.tool_instructions = tool_instructions
        self.func_tools_dict = {}
        self.tools = []
        self.client = OpenAI(api_key=api_key)
        self.input_list = []

    def run_agent_stream(self, message: str):
        self.input_list.append({"role": "system", "content": self.context})
        self.input_list.append({"role": "user", "content": message})

        Logger.log("Starting streaming_agent_run")

        # 1️⃣ Stream initial response
        with self.client.responses.stream(
            model="gpt-5",
            input=self.input_list,
            tools=self.tools,
        ) as stream:

            for event in stream:
                if event.type == "response.output_text.delta":
                     yield event.delta  # ✅ STREAM TO CLIENT

                elif event.type == "response.output_item.added":
                    if event.item.type == "function_call":
                        self.input_list.append(event.item)

            response = stream.get_final_response()

        self.input_list += response.output

        # 2️⃣ Execute tools
        for item in response.output:
            if item.type == "function_call":
                tool = self.func_tools_dict[item.name]
                args = json.loads(item.arguments)
                result = tool(**args)   

                self.input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({item.name: result})
                })

        # 3️⃣ Stream final answer
        with self.client.responses.stream(
            model="gpt-5",
            instructions=self.tool_instructions,
            input=self.input_list,
            tools=self.tools,
        ) as stream:

            for event in stream:
                if event.type == "response.output_text.delta":
                    yield event.delta  # ✅ STREAM TO CLIENT

            final_response = stream.get_final_response()
            return final_response.output_text


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

    def add_tool(self, func):
        self.tools.append(function_to_tool_schema(func))
        self.func_tools_dict[func.__name__] = func


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
    d = {
        "type": "function",
        "name": func.__name__,
        "description": func.__doc__ or "",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }
    print(d)
    return d