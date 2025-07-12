import os
from dotenv import load_dotenv
import logging
import sys
import azure.functions as func
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from PriceAlgorithm.factors import generateTarrif
from azure.cosmos import CosmosClient
from ModelRunner.getWeatherData import get_current_time


def upload_data():
    load_dotenv()
    primary_key = os.getenv('COSMOS_DB_KEY')
    database_url = os.getenv('COSMOS_DB_URL')
    database_name = os.getenv('DATABASE')
    container_name = 'Energy_Price'
    
    client = CosmosClient(database_url,primary_key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    
    _,_,date_list = get_current_time()
    price_arr = generateTarrif()
    logging.info('Storing started')
    for idx,price in enumerate(price_arr):
        container.upsert_item({
            'id' : str(date_list[idx]),
            'Location' : 'UoM',
            'price' : price
        })
    logging.info('Storing ended')

app = func.FunctionApp()

@app.timer_trigger(schedule="0 5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def DevEnergyMarktePriceUpload(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    upload_data()
    logging.info('Python timer trigger function executed.')