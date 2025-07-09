from dataPreprocessing import create_input_rf,load_scaler,get_historical_generation,create_input_lstm
from getWeatherData import get_weather_data,weather_data_to_dataframe
import pickle
from keras.models import load_model
import numpy as np

def load_Model(type):
    if type == 'genRF':
        with open('ModelRunner/rf_model.pkl', 'rb') as f:
            model= pickle.load(f)
    if type == 'genLSTM':
        model = load_model('ModelRunner/24-0.0019.ckpt')
    
    return model

def run_RF():
    rf_input = create_input_rf()
    rf_model = load_Model('genRF')
    genScaler = load_scaler('gen')
    predictions = rf_model.predict(rf_input)
    predictions_non_scaled = genScaler.inverse_transform([predictions])
    return predictions_non_scaled


def run_lstm():
    predictionsArr = []
    model = load_Model('genLSTM')
    genScaler = load_scaler('gen')
    irrScaler = load_scaler('irr')
    query = get_historical_generation()
    x,genArr,irrArr = create_input_lstm(query)
    x = np.expand_dims(x, axis=0)
    
    weatherJson = get_weather_data()
    _,weather_df = weather_data_to_dataframe(weatherJson)
    weather_df['solarradiation'] = irrScaler.transform(weather_df[['solarradiation']])
    irrForecastArr = weather_df['solarradiation'].to_list()
    
    for i in range(24):
        predictions = model.predict(x)
        predictionsArr.append(genScaler.inverse_transform(predictions).flatten()[0])
        
        genArr.append(predictions.flatten()[0])
        genArr = genArr[1:]
        irrArr.append(irrForecastArr[i])
        irrArr = irrArr[1:]
        x = np.array([genArr,irrArr])
        x = np.expand_dims(x, axis=0)
        
    return irrForecastArr







