import os
import logging
import azure.functions as func
import requests
from dotenv import load_dotenv
from azure.cosmos import CosmosClient



def upload_demand_forecast():
    url = 'http://127.0.0.1:8000/getDemandForecast'
    
    response = requests.get(url)
    response = response.json()
    data_arr = response['demandForecast']
        
    load_dotenv()
    primary_key = os.getenv('COSMOS_DB_KEY')
    database_url = os.getenv('COSMOS_DB_URL')
    database_name = os.getenv('DATABASE')
    container_name = 'demandForecast'

    client = CosmosClient(database_url,primary_key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    
    for entry in data_arr:
        container.upsert_item({
            'id' : str(entry['time']),
            'Location' : 'UoM',
            'demand' : round(entry['demand'],2)
    })
        

app = func.FunctionApp()

@app.timer_trigger(schedule="0 5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def DevEnergyMarketDemandForecast(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    upload_demand_forecast()
    logging.info('Python timer trigger function executed.')