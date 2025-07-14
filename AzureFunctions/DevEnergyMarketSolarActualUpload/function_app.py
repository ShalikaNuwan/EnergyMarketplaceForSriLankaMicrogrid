import os
import sys
import logging
import azure.functions as func
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from ModelRunner.getWeatherData import weather_data_to_dataframe,get_weather_data,get_current_time

def generation_of_hour():
    weather_json = get_weather_data()
    df,_ = weather_data_to_dataframe(weather_json)
    _,previous_hour,_ = get_current_time()

    df = df[df.index == previous_hour]
    generation = round((df['solarradiation']*(257.27/1000)*0.9/6.43).to_list()[0],2)
    irradiation = df['solarradiation'].to_list()[0]
    
    return generation,previous_hour,irradiation

def fetch_data():
    load_dotenv()
    primary_key = os.getenv('COSMOS_DB_KEY')
    database_url = os.getenv('COSMOS_DB_URL')
    database_name = os.getenv('DATABASE')
    container_name = os.getenv('CONTAINER')

    client = CosmosClient(database_url,primary_key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    
    solar_gen,previous_hour,irr = generation_of_hour()
    logging.info('Storing started')
    logging.info(f'data stored for {previous_hour}')
    container.upsert_item({
        'id' : previous_hour,
        'Location' : 'UoM',
        'SolarGeneration' : solar_gen,
        'irradiation' : irr
        
    })
    logging.info('Storing ended')
    
    
app = func.FunctionApp()

@app.timer_trigger(schedule="0 2 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def DevEnergyMarketSolarActualUpload(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    fetch_data()

    logging.info('Python timer trigger function executed.')