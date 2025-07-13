import os
import json
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from fastapi import FastAPI
from ModelRunner.modelRunner import run_hybrid,runDemandLSTM
from ModelRunner.getWeatherData import get_current_time
from fastapi.middleware.cors import CORSMiddleware
from ModelRunner.getDataFromDatabase import get_current_price,get_price_forecast,get_actual_predictions,getSolarForecast



app = FastAPI()
   
origins = [
    "http://localhost:8080",  # React dev server
    "http://172.20.10.3:8080",
    "http://127.0.0.1:8000",
    "http://10.10.42.251:8080",
    "http://172.20.10.3:8080/",
    "http://172.20.10.3:8080/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/GetSolarForecast')
def GetSolarForecast():
    print("here")
    # _,_,date_list = get_current_time()
    date_list,solar_fcst_list = getSolarForecast()

    endpoint_arr = []
    for index,solarGen in enumerate(solar_fcst_list):
        temp_dict = {
            'time' : date_list[index],
            'output' : round(float(solarGen),2)
        }
        endpoint_arr.append(temp_dict)
    
    return {'solarForecast' : endpoint_arr}

@app.get('/getDemandForecast')
def getDemandForecast():
    # _,_,date_list = get_current_time()
    date_list,_,demand_fcst_list,_,_ = get_actual_predictions()
    
    endpoint_arr = []
    for index,dem in enumerate(demand_fcst_list):
        temp_dict = {
            'time' : date_list[index],
            'demand' : round(float(dem),2)
        }
        endpoint_arr.append(temp_dict)
    
    return {'demandForecast' : endpoint_arr}

@app.get("/")
def health():
    return {"msg":"server running sucessfully"}

@app.get('/getCurrentPrice')
def getCurrentPrice():
    price = get_current_price()
    return {"currentMarketPrice": round(price,2)}

@app.get('/priceForecast')
def getPriceForecast():
    date_list, price_list = get_price_forecast()
    price_arr = []
    print(price_list)
    for idx,price in enumerate(price_list):
        temp_dict = {
            "time" : date_list[idx],
            "price" : price
        }
        price_arr.append(temp_dict)
    return {"hourlyForecast": price_arr}
    
@app.get('/getPastMatchedEnergy')
def getPastMatchedEnergy():
    with open('final_profile.json', "r") as file:
        data = json.load(file)
    
    final_arr = []
    _,_,date_list = get_current_time()
    print(len(date_list))
    print(len(data['matched_results']))
    print(date_list)
    for idx,datetime in enumerate(date_list):
        temp_dict = {
            'time' : datetime,
            'demand' : round(data['matched_results'][idx]['demand'],1),
            'solar' : round(data['matched_results'][idx]['solar'],1),
            'battery' : round(data['matched_results'][idx]['battery_usage'],1),
            'diesel' : round(data['matched_results'][idx]['generator_capacity'],1)  
        }
        final_arr.append(temp_dict)
    
    return {"pastDemandSupply": final_arr}
   
@app.get('/getPaseActualPredictions')    
def getActualPredictions():
    date_list,solar_fcst_list,demand_fcst_list,solar_act_list,demand_act_list = get_actual_predictions()
    
    final_arr = []
    for idx,date in enumerate(date_list):
        temp_dict = {
            "time" : date,
            "forecastDemand": demand_fcst_list[idx],
            "actualDemand": demand_act_list[idx],
            "forecastSolar": solar_fcst_list[idx],
            "actualSolar": solar_act_list[idx]
        }
        final_arr.append(temp_dict)
        
    return {"comparisonData": final_arr}
    

