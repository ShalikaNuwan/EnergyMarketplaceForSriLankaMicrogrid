from datetime import datetime, timezone,timedelta

now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
formatted_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")

#pd.date_range(start=formatted_time, periods=24, freq='H').strftime("%Y-%m-%dT%H:%M:%SZ").tolist()
timestamps = [
        (now + timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        for i in range(24)
    ]

timestamps_past = [
        (now - timedelta(hours=i)).strftime("%Y-%m-%dT%H:%M:%SZ")
        for i in range(24)
    ]


#demand forecasting chart
def DemandForecasting(demand):
    arr_demand =[]
    dict_demand = {}

    for i in range(24):
        dict_demand = {
            "time": timestamp[i],
            "demand": demand[i],
            "unit": "kWh"
        }
        arr_demand.append(dict_demand)
    
    return(arr_demand)
    
#solar forecasting chart   
def SolarForecasting(solar_gen):
    arr_solar =[]
    dict_solar = {}

    for i in range(24):
        
        dict_solar = {
            "time": timestamp[i],
            "solar": solar_gen[i],
            "unit": "kW"
        }
        arr_solar.append(dict_solar)
    
    return(arr_solar)

#price forecasting chart
def PriceForecasting(price):
    arr_price =[]
    dict_price = {}

    for i in range(24):
        
        dict_solar = {
            "time": timestamp[i],
            "price": price[i],
            "unit": "LKR/kWh"
        }
        arr_price.append(dict_price)
    
    return(arr_price)


#demand and supply balance in past 24 hours
def DemandSupplyBalance(demandForecasted, solarForecasted):
    arr =[]
    dict = {}
    
    for i in range(24):
        solar_excess,solar_excess_energy,battery_usage,chargingStatus,remaininCharge,demand_shortage,demand_shortage_amount = getBatteryAllocation(solar_generation_kw[i],demand[i],init_stage,0.2,0.96)
        
        dict = {
            "time": timestamps_past[i],
            "demand": demandForecasted[i],
            "solar": solarForecasted[i],
            "battery": battery_usage,   # past 24 hours needs to be applied
            "diesel": demand_shortage_amount # past 24 hours needs to be applied
            
        }
        arr.append(dict)
    return(arr)

#Price display for a specific hour
def Price(price):
    dict_HourlyPrice = {
        "price": price[0],
        "trend": {
            "direction": "down" if price[0] > price[1] else "up",
            "percentage": abs(price[0] - price[1]) / price[0] * 100,
            "lastUpdated": formatted_time
        }
    }
    return dict_HourlyPrice

#price display for next 24 hours
def PriceforNextHours(price):
    dict_NextHoursPrice = {}
    arr_NextHoursPrice = []
    
    for i in range(24):
        dict_NextHoursPrice = {
            "time": timestamp[i],
            "price": price[i]
        }
        arr_NextHoursPrice.append(dict_NextHoursPrice)
    return arr_NextHoursPrice

    
    


#Forecasted and actual comparison charts for solar generation and demand
def ForecastedActual(demandForecasted,demandActual, solarForecasted, solarActual):
    arr =[]
    dict = {}
    
    for i in range(24):
        dict = {
            "time": timestamp[i],
            "forecastDemand": demandForecasted[i],
            "actualDemand": demandActual[i],
            "forecastSolar": solarForecasted[i],
            "actualSolar": solarActual[i]
            
        }
        arr.append(dict)
    return(arr)

    


