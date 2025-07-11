import os
import json
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from fastapi import FastAPI
from ModelRunner.modelRunner import run_hybrid,runDemandLSTM
from ModelRunner.getWeatherData import get_current_time


app = FastAPI()
   
@app.get('/GetSolarForecast')
def GetSolarForecast():
    _,_,date_list = get_current_time()
    solar_forecast = run_hybrid()
    
    endpoint_arr = []
    for index,solarGen in enumerate(solar_forecast):
        temp_dict = {
            'Datetime' : date_list[index],
            'Generation' : round(float(solarGen),2)
        }
        endpoint_arr.append(temp_dict)
    
    return {'predictions' : endpoint_arr}

@app.get('/getDemandForecast')
def getDemandForecast():
    _,_,date_list = get_current_time()
    demand_forecast = runDemandLSTM()
    
    endpoint_arr = []
    for index,dem in enumerate(demand_forecast):
        temp_dict = {
            'Datetime' : date_list[index],
            'Demand' : round(float(dem),2)
        }
        endpoint_arr.append(temp_dict)
    
    return {'predictions' : endpoint_arr}
    