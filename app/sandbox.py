# from pymongo import MongoClient

# client = MongoClient("mongodb://root:example@mongo:27017")
# db = client["mydb"]

# print(list(db["users"].find()))


## test api key
# from agent import MedicineAsisstentAgent

# open_ai_apy_key = "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"

# ag = MedicineAsisstentAgent()
# msg = "my name is gal, how are you?"
# respond = ag.invoke(msg)
# print(respond.json())



import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_ready",
        "description": "does nothing.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia",
                }
            },
            "required": ["location"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

response = client.responses.create(
    model="gpt-5",
    input=[
        {"role": "user", "content": "What is the weather like in Paris today?"},
    ],
    tools=tools,
)

print(response.output)