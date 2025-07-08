from dataPreprocessing import create_input_rf,load_scaler
import pickle

def load_Model(type):
    if type == 'genRF':
        with open('ModelRunner/rf_model.pkl', 'rb') as f:
            loaded_model= pickle.load(f)
    if type == 'genLSTM':
        pass
    
    return loaded_model
def run_RF():
    rf_input = create_input_rf()
    rf_model = load_Model('genRF')
    genScaler = load_scaler('gen')
    predictions = rf_model.predict(rf_input)
    predictions_non_scaled = genScaler.inverse_transform([predictions])
    return predictions_non_scaled









