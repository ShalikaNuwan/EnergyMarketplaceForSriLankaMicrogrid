import os
from azure.cosmos import CosmosClient
from datetime import datetime
from dotenv import load_dotenv
from ModelRunner.dataPreprocessing import load_database
from ModelRunner.getWeatherData import get_current_time

def get_current_price():
    container = load_database('price')
    current_datetime,_,_ = get_current_time()
    dt = datetime.fromisoformat(current_datetime)
    current_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
    next_day_query = f"""
    SELECT * FROM c
    WHERE c.id = '{current_datetime}'
    """
    current_price = list(container.query_items(
        query=next_day_query,
        enable_cross_partition_query=True
    ))
    
    return current_price[0].get('price')

def get_price_forecast():
    container = load_database('price')
    current_datetime,_,_ = get_current_time()
    dt = datetime.fromisoformat(current_datetime)
    current_datetime = dt.strftime("%Y-%m-%d %H:%M:%S")
    next_day_query = f"""
    SELECT * FROM c
    WHERE c.id >= '{current_datetime}'
    """
    current_price = list(container.query_items(
        query=next_day_query,
        enable_cross_partition_query=True
    ))
    print('response',current_price)
    date_list = [entry["id"] for entry in current_price]
    price_list = [round(entry["price"],2) for entry in current_price]
    print(price_list)
    print(date_list)
    return date_list,price_list

def get_actual_predictions():
    solar_fcst_list = []
    demand_fcst_list = []
    solar_act_list = []
    demand_act_list = []
    
    total_arr = [solar_fcst_list,demand_fcst_list,solar_act_list,demand_act_list]
    container_names = ['solarFCST','demandFCST','solarActual','demand']
    unit_arr = ['solarForecast','demand','SolarGeneration','redistributed']
    current_datetime,_,_ = get_current_time()

    for idx,container_name in enumerate(container_names):
        container = load_database(container_name)
        next_day_query = f"""
        SELECT * FROM c
        WHERE c.id < '{current_datetime}'
        ORDER BY c.id DESC
        OFFSET 0 LIMIT 24
        """
        response = list(container.query_items(
            query=next_day_query,
            enable_cross_partition_query=True
        ))
        response = response[::-1]
        date_list = [entry["id"] for entry in response]
        
        if container_name == 'solarFCST':
            solar_fcst_list = [entry["solarForecast"] for entry in response]
        elif container_name == 'demandFCST':
            demand_fcst_list = [entry["demand"] for entry in response]
        elif container_name == 'solarActual':
            solar_act_list = [entry["SolarGeneration"] for entry in response]
        else:
            demand_act_list = [entry["redistributed"] for entry in response]
                 
    return date_list,solar_fcst_list,demand_fcst_list,solar_act_list,demand_act_list

def getSolarForecast():
    container = load_database('solarFCST')
    current_datetime,_,_ = get_current_time()
    
    next_day_query = f"""
        SELECT * FROM c
        WHERE c.id >= '{current_datetime}'
        """
    response = list(container.query_items(
        query=next_day_query,
        enable_cross_partition_query=True
    ))
    
    date_list = [entry["id"] for entry in response]
    gen_list = [round(entry["solarForecast"],2) for entry in response]
    
    return date_list,gen_list