from getWeatherData import get_weather_data,weather_data_to_dataframe
import pickle
from sklearn.preprocessing import LabelEncoder



#data preprocessing for the RandomForest model
def load_scaler(type):
    if type == 'gen':
        with open('ModelRunner/genScalerRF.pkl', 'rb') as f:
            loaded_scaler = pickle.load(f)

    return loaded_scaler


def load_label_encoders(type):
    if type == 'WeatherConditions':
        with open('ModelRunner/label_encoder_weather_condition.pkl', 'rb') as f:
            loaded_lable_encoder = pickle.load(f)
    
    return loaded_lable_encoder


def create_input_rf():
    weatherJson = get_weather_data()
    weather_df = weather_data_to_dataframe(weatherJson)
    weather_encoder = load_label_encoders('WeatherConditions')
    weather_df['conditions_encoded'] = weather_encoder.transform(weather_df['conditions'])
    weather_df['month'] = weather_df.index.month
    weather_df['day'] = weather_df.index.day
    weather_df['day_of_week'] = weather_df.index.day_of_week
    weather_df['day_of_year'] = weather_df.index.day_of_year
    x = weather_df[['temp','humidity','windgust','solarradiation','conditions_encoded','month','day','day_of_week','day_of_year']]
    
    return x
    
    
    
    
    
    
#data preprocessing for the LTSM model

