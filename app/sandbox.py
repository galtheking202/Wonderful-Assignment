from agent_utils.tools import get_medicine_data_by_name,TOOLS

from agent_utils.base_agent import BaseAgent
import pprint

agent = BaseAgent()
agent.add_tool(get_medicine_data_by_name.__name__, get_medicine_data_by_name)
pprint.pprint(agent.tools[0])
pprint.pprint(TOOLS[0])