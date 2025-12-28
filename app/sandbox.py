from agent_utils.tools import *
from agent_utils.base_agent import BaseAgent
import pprint

agent = BaseAgent()
agent.add_tool(get_medicine_by_name.__name__, get_medicine_by_name)