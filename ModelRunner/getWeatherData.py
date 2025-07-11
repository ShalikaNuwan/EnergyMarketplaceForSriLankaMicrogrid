import os
import requests
import sys
import pandas as pd
import json
from dotenv import load_dotenv
from datetime import datetime,timedelta

def get_current_time():
    current_time = datetime.now()
    previous_hour = current_time - timedelta(hours=1)
    endtime = current_time + timedelta(hours=24)
    filter_date = datetime(current_time.year, current_time.month, current_time.day, current_time.hour, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
    previous_hour_str = datetime(previous_hour.year, previous_hour.month, previous_hour.day, previous_hour.hour, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
    endtime_str = datetime(endtime.year, endtime.month, endtime.day, endtime.hour, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
    datetime_list = pd.date_range(start=filter_date, end=endtime_str, freq='h')
    return filter_date,previous_hour_str,datetime_list

 
def get_weather_data():
    load_dotenv()
    weatherAPIKey = os.getenv('WEATHER_API_KEY')
    response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Moratuwa%2C%20Sri%20Lanka/next24hours?unitGroup=metric&include=hours&key={weatherAPIKey}&contentType=json")
    if response.status_code!=200:
        print('Unexpected Status code: ', response.status_code)
        sys.exit()  
        
    jsonData = response.json()
    return jsonData
    

def weather_data_to_dataframe(weather_json: dict) -> pd.DataFrame:
    rows = []

    for day in weather_json.get("days", []):
        date_str = day["datetime"]                   
        for hr in day.get("hours", []):
            ts = f"{date_str}T{hr['datetime'][:5]}"     
            row = {"datetime": ts}

            row.update({k: v for k, v in hr.items() if k != "datetime"})
            rows.append(row)

    df = pd.DataFrame(rows)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index('datetime',inplace=True)
    filter_date,_ = get_current_time()
    filered_df = df[df.index >= filter_date].head(24)
    return df,filered_df

