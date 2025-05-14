import os
import json
from dotenv import load_dotenv
from EMS.agents import EMSAgent
from langchain_openai import AzureChatOpenAI



load_dotenv()
model = AzureChatOpenAI(
    azure_endpoint=os.getenv("ENDPOINT"),
    azure_deployment="gpt-4.1",
    openai_api_version="2024-12-01-preview",
    api_key=os.getenv("KEY")
)
Solar_generation = [0, 0, 0, 0, 0, 0, 0, 0,3.700453992, 12.26994969, 16.59675193, 23.49084165,28.15493203, 27.3358267, 28.49920984, 24.18710535,18.38220007, 8.992326684, 5.780816585, 0.949614256,0, 0, 0]
demand = [4.52927534, 4.078508217, 4.024205961, 3.954138532, 3.905091332, 3.810500305,3.946547894, 3.920272609, 6.356867425, 1.8013168, 8.87812705, 5.667287152,6.08302056, 5.586709611, 5.71166319, 5.278996823, 8.386487262, 6.880037554,11.99256585, 17.52468125, 23.29333262, 12.96364201, 9.831627969, 4.307296]
battery_soc = 60
                        
testAgent = EMSAgent(model=model)
output = testAgent.execute(Solar_generation,demand,battery_soc)

with open("matched_energy.json", "w") as f:
    json.dump(output, f, indent=2)