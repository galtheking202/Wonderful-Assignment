from .contexts import *
from .tools import *
from .base_agent import BaseAgent
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = "https://api.openai.com/v1/responses"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class MedicineAssistantAgent(BaseAgent):
    def __init__(self, context: str = AGENT_CONTEXT, tool_instructions: str = TOOL_INSTRUCTIONS, api_key: str = OPENAI_API_KEY):
        super().__init__(context=context, tool_instructions=tool_instructions, api_key=api_key)
        self.add_tool(get_client_prescriptions)
        self.add_tool(get_medicine_by_name)
        self.add_tool(purchase_medicine)
        # self.add_tool(get_medicine_by_id)
        # self.add_tool(login_user)
        

