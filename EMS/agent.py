from crewai import Agent
from llm import llm
from crewai.tools import tool
from ModelRunner.modelRunner import run_hybrid,runDemandLSTM


@tool('getSolarData')
def get_solar_data() -> list:
    """Returns hourly solar generation data for the microgrid in kWh."""
    return run_hybrid()

@tool('getDemandData')
def get_demand_data() -> list:
    """Returns hourly energy demand data for the microgrid in kWh."""
    return runDemandLSTM()

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
    
