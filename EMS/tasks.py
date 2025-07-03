from crewai import Task
from agent import ems_agent,genAgent,battery_agent
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List

class HourlyMatch(BaseModel):
    time : str
    solar : float
    demand : float
    solar_excess : bool
    solar_excess_energy : float
    battery_usage: float
    charging_status : bool
    soc : float
    demand_shortage : bool
    demand_shortage_amount : float
    generator_used : bool
    generator_capacity : float
    
class EMSMatchProfile(BaseModel):
    matched_results: List[HourlyMatch]

parser = PydanticOutputParser(pydantic_object=EMSMatchProfile)

ems_matching = Task(
    description=(
        "gather the next 24 hours of solar generation, demand for the microgroid."
        "gather the initial battery soc of the battery."
        "The task is to match the demand and supply for the microgrid."
        """Here are the scenarios that you need to work.
            1. solar generation is grater than the demand.
                i) if the excess solar is enogh to charge the battery the allocate that excess energy to the battery.
                ii) Always check the excess energy grater than the battery capacity that needed to fullly charge the battery. if that is grater, then allocate the needed energy to the batery and give me an message that there are exsisting solar remaining.
                
            2. Solar generation is lower than the demand.
                i) if the solar generation is lower than the demand, then allocate the shortage amount from the battery if the battery has enough energy.
                ii) if the battery is not enough (battery at the minimum soc level) then turn on the diesel generator and run it to meet the demand.
        the batery capacity is 288kWh. maximum soc is '96%' and minumum soc is 30%. 
            the capacity of the generator is 50kWh.
            You need to match the demand and supply using the provided solar generation and demand array
            the battery usage is positive if the battery is discharged. Otherwise it's negative value. The battery Soc value cannot be grater than '96%' and less than 30%.
            Solar_Excess valus need to determined after allocating the energy to the battery."""
    ),
    expected_output="JSON file containing the next 24 hours hourly matched energy profiles with the structure of " + parser.get_format_instructions(),
    agent=ems_agent,
    output_file='ems.json'
)


optimum_gen_level = Task(
    description=(
        "The task is to run the diesel generaytor at the optimum level to meet the demand."
        "the diesel generator capacity is 50kWh."
        "there are four levels of diesel generator running. which are 0.25,0.5,0.75, and 1."
        "consider the enrgy matched by the ems agent."
        "If there is any usage in the generator, use above levels to decide the optimum level."
        "after set the working level of the generator, if there is any excess enery from the generator, then allocate that energy to the battery and set the soc considering the stored energy."
    ),
    expected_output="JSON file containing the next 24 hours hourly matched energy profiles with the structure of " + parser.get_format_instructions(),
    context=[ems_matching],
    agent=genAgent,
    output_file='optimum_gen.json'
)

final_profile = Task(
    description=(
        "The task is to Calculate the final soc level of the batery considering the Generator surplus."
        "consider the optimum_gen.json file and if the generator_used is true then do the following tasks."
        "the soc in each hour is the end soc after working in that hour."
        "The generator is working at some constant levels which can be greater than the demand_shortage_amount in each hour."
        "you need to calculate the excess energy due to the generator and allocate that energy to the battery. Then calculate the new soc."
        "the optimum_gen.json gives the soc as a percentage value, so you need to convert that to kWh value (battery capacity is 288kWh) and the allocate the surplus energy to get the final value and then devide 288 to get the new soc."
        ""
    ),
    expected_output="JSON file containing the next 24 hours hourly matched energy profiles with the structure of " + parser.get_format_instructions(),
    context=[optimum_gen_level],
    agent=battery_agent,
    output_file='final_profile.json'
    
    
)
tasks: list[Task] = [ems_matching,optimum_gen_level,final_profile]
__all__ = ['tasks']