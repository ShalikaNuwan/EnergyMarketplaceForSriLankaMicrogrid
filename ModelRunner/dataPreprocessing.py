from getWeatherData import get_weather_data,weather_data_to_dataframe,get_current_time
import pickle
from sklearn.preprocessing import LabelEncoder
import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
import pandas as pd
import numpy as np

#data preprocessing for the RandomForest model
def load_scaler(type):
    if type == 'gen':
        with open('ModelRunner/genScalerRF.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)
    if type == 'irr':
        with open('ModelRunner/irrScaler.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)
    if type == 'nn':
        with open('ModelRunner/nnScaler.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)
    if type =='rf':
        with open('ModelRunner/predrfScaler.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)
    if type == 'lstm':
        with open('ModelRunner/predLstmScaler.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)
    if type == 'demand':
        with open('ModelRunner/demandScaler.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)
    return loaded_scaler


def load_label_encoders(type):
    if type == 'WeatherConditions':
        with open('ModelRunner/label_encoder_weather_condition.pkl', 'rb') as f:
            loaded_lable_encoder = pickle.load(f)
    
    return loaded_lable_encoder


def create_input_rf():
    weatherJson = get_weather_data()
    _,weather_df = weather_data_to_dataframe(weatherJson)
    weather_encoder = load_label_encoders('WeatherConditions')
    weather_df['conditions_encoded'] = weather_encoder.transform(weather_df['conditions'])
    weather_df['month'] = weather_df.index.month
    weather_df['day'] = weather_df.index.day
    weather_df['day_of_week'] = weather_df.index.day_of_week
    weather_df['day_of_year'] = weather_df.index.day_of_year
    x = weather_df[['temp','humidity','windgust','solarradiation','conditions_encoded','month','day','day_of_week','day_of_year']]
    
    return x
       
#data preprocessing for the LTSM model
def load_database(type):
    load_dotenv()
    primary_key = os.getenv('COSMOS_DB_KEY')
    database_url = os.getenv('COSMOS_DB_URL')
    database_name = os.getenv('DATABASE')
    if type == 'solarActual':
        container_name = 'Solar Generation'
    if type == 'demand':
        container_name = 'demand'
    client = CosmosClient(database_url,credential=primary_key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container

def get_historical_generation():
    container = load_database('solarActual')
    _,last_hour,_ = get_current_time()
    
    next_day_query = f"""
    SELECT TOP 48 * FROM c
    WHERE c.id <= "{last_hour}" 
    ORDER BY c.id DESC
    """
    last_48_hours_generation = list(container.query_items(
        query=next_day_query,
        enable_cross_partition_query=True
    ))
    
    return last_48_hours_generation[::-1]
    

def create_input_lstm(query_output):
    df = pd.DataFrame(query_output)
    genScaler = load_scaler('gen')
    irrScaler = load_scaler('irr')
    df = df.rename(columns={'SolarGeneration': 'Adjusted_Generation'})
    df = df.rename(columns={'irradiation': 'solarradiation'})
    df['Adjusted_Generation'] = genScaler.transform(df[['Adjusted_Generation']])
    df['solarradiation'] = irrScaler.transform(df[['solarradiation']])
    
    genArr = df['Adjusted_Generation'].to_list()
    irrArr = df['solarradiation'].to_list()
    x = np.array([genArr,irrArr])
    
    return x,genArr,irrArr

#data preprocessing for demand LSTM model
def download_demand_data():
    container = load_database('demand')
    _,last_hour,_ = get_current_time()
    
    next_day_query = f"""
    SELECT TOP 48 * FROM c
    WHERE c.id <= "{last_hour}"
    ORDER BY c.id DESC 
    """
    last_48_hours_demand = list(container.query_items(
        query=next_day_query,
        enable_cross_partition_query=True
    ))
    
    return last_48_hours_demand[::-1]
    

def create_demand_sequence():
    demand_df = pd.DataFrame(download_demand_data())
    scaler = load_scaler('demand')
    demand_df['redistributed'] = scaler.transform(demand_df[['redistributed']])
    sequence = demand_df['redistributed'].to_list()
    
    return sequence
    
