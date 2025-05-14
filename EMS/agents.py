from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from typing import List
import json

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

class EMSAgent:
    def __init__(self,model):
        self.parser = PydanticOutputParser(pydantic_object=EMSMatchProfile)
        self.ems_system_prompt = PromptTemplate(
        template=(
            '''
            You are a Energy expert who is capable of matching the demand and supply of microgrid. The task is to match the demand and supply for the microgrid. 
            you will get the solar generation, demand, battery capacity, and the size of the generator.
            Here are the scenarios that you need to work.
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
            Solar_Excess valus need to determined after allocating the energy to the battery.
            '''
            "Return the matched data in the following format:\n{format_instructions}\n\n"
            "Here is the input data:\n{input_data}"
        ),
        input_variables=["input_data"],
        partial_variables={"format_instructions": self.parser.get_format_instructions()}
        
        )
        self.model = model
        self.input_query = """ Solar generation = {}
                        demand = {}
                        initial battery_soc = {}%"""
                        
    def execute(self,solar_arr,demand_arr,battery_soc):
        query = self.input_query.format(solar_arr,demand_arr,battery_soc)
        formatted_prompt = self.ems_system_prompt.format(input_data=query)
        response = self.model.invoke(formatted_prompt)
        structured_output = self.parser.parse(response.content)
        json_data = [record.dict() for record in structured_output.matched_results]
        return json_data
        
