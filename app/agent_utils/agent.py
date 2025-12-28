from contexts import AGENT_CONTEXT
from .base_agent import BaseAgent
from dotenv import load_dotenv
from .tools import *
import os

load_dotenv()

API_URL = "https://api.openai.com/v1/responses"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class MedicineAssistantAgent(BaseAgent):
    def __init__(self, context: str = AGENT_CONTEXT, api_key: str = OPENAI_API_KEY):
        super().__init__(context=context, api_key=api_key)
        self.add_tool(get_client_prescriptions)
        self.add_tool(get_medicine_by_name)
        self.add_tool(purchase_medicine)
        # self.add_tool(get_medicine_by_id)
        # self.add_tool(login_user)
        

