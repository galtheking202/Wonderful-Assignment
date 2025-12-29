import os
os.environ["RUN_ENV"] = "local" # Set environment to local for testing

from agent_utils.agent import MedicineAssistantAgent
import pandas as pd
from logger import LOG_BUFFER

df = pd.read_excel("agent_evaluation_prompts.xlsx")

import pandas as pd

results = []

for idx, row in df.iterrows():
    user_prompt = row["User_Prompt"]
    agent = MedicineAssistantAgent()

    full_response = ""
    for chunk in agent.run_agent_stream(user_prompt):
        full_response += chunk
    print(f"Completed Prompt ID {idx}")
    results.append({
        "Prompt_ID": idx,
        "User_Prompt": user_prompt,
        "Expected_Tools": row["Expected_Tools"],
        "Tools_Called": ",".join(LOG_BUFFER[1:]), # Skip the first log entry which is usually the start log
        "Agent_Response": full_response,
        "Test_type":row["Test_type"],
    })

    # 🔹 SAVE CHECKPOINT EACH ITERATION
    pd.DataFrame(results).to_excel("agent_evaluation_prompts_output.xlsx", index=False)

    LOG_BUFFER.clear() # Clear logs for the next iteration



