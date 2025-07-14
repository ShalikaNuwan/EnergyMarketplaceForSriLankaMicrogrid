import os
import sys
import logging
import azure.functions as func
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from EMS.crew import runEMS
import json
from ModelRunner.dataPreprocessing import load_database
from ModelRunner.getWeatherData import get_current_time

def uplaodSOC():
    runEMS()
    
    with open('final_profile.json', "r") as file:
        data = json.load(file)
    
    container = load_database('soc')
    _,_,date_list = get_current_time()
    
    for idx,date in enumerate(date_list):
        container.upsert_item({
            'id' : str(date_list[idx]),
            'Location' : 'UoM',
            'soc' : round(data['matched_results'][idx]['soc'],2)
        })
    
    
    
app = func.FunctionApp()

@app.timer_trigger(schedule="0 5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def DevEnergyMarketSocLevelStore(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    uplaodSOC()
    logging.info('Python timer trigger function executed.')