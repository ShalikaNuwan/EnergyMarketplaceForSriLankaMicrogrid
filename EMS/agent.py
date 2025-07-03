from crewai import Agent
from llm import llm
from crewai.tools import tool

@tool('getSolarData')
def get_solar_data() -> list:
    """Returns hourly solar generation data for the microgrid in kWh."""
    return [0, 0, 0, 0, 0, 0, 0, 0,3.700453992, 0, 0, 3.49084165,8.15493203, 7.3358267, 8.49920984, 4.18710535,8.38220007, 3.992326684, 5.780816585, 0.949614256,0, 0, 0]

@tool('getDemandData')
def get_demand_data() -> list:
    """Returns hourly energy demand data for the microgrid in kWh."""
    return [4.52927534, 4.078508217, 4.024205961, 3.954138532, 3.905091332, 3.810500305,3.946547894, 3.920272609, 6.356867425, 1.8013168, 8.87812705, 5.667287152,6.08302056, 5.586709611, 5.71166319, 5.278996823, 8.386487262, 6.880037554,11.99256585, 17.52468125, 23.29333262, 12.96364201, 9.831627969, 4.307296]

@tool('getBatterySoc')
def get_battery_soc() -> float:
    """Returns the battery soc level for the initial hour."""
    return 40

ems_agent = Agent(
    role="Expert Energy Manager",
    goal=("Match the demand and supply for microgrid"
          "The microgrid powered by solar, battery, and diesel generators."
        "Your main responsibility is to match the demand by using the solar energy."
        "If the solar energy is not enough, you can use the battery."
        "If the battery is not enough, you can use the diesel generator."
        "when there is a surplus of solar energy, you can charge the battery."
        "if the battery is full, the price should be reduced to use that energy."
          ),
    backstory=(
        "You are an expert in managing the demand and supply of islanded microgrids."
        "You have a deep understanding of the energy management system and its components."
        "You are familiar with the solar energy, battery, and diesel generators."
    ),
    llm=llm,
    tools=[get_solar_data, get_demand_data, get_battery_soc]
)

genAgent = Agent(
    role="Expert of Running Diesel Generator",
    goal="Run the diesel generator at the optimum level to meet the demand.",
    backstory=(
        "You are an expert in running the diesel generator at its optimum level."
    ),
    llm=llm
)

battery_agent = Agent(
    role="Expert of Battery Management",
    goal="Manage battery soc level considering the solar surlus or generator surplus.",
    backstory=(
        "You are an energy expert who knows how to run the battery and calculate the battery soc correcly."
    ),
    llm=llm
)

agents: list[Agent] = [ems_agent,genAgent,battery_agent]

__all__ = ['agents','ems_agent','genAgent']
    
