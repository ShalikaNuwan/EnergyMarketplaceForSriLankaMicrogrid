solar_generation_kw = [0, 0, 0, 0, 0, 0, 5, 15, 35, 50, 55, 58, 60, 58, 55, 50, 35, 15, 5, 0, 0, 0, 0, 0]
demand = [4.52, 4.078, 4.024, 3.95, 3.905, 3.81, 3.94, 3.92, 6.35, 1.80, 8.87, 5.66, 6.08, 5.58, 5.711, 5.27, 8.38, 6.88, 11.99, 17.52, 23.29, 12.96, 9.83, 6.59]

battery_capacity = 300

def getChargingStatus(usage):
    is_charging = lambda usage : usage > 0
    return is_charging(usage)


def getBatteryAllocation(solar_gen,demand,intial_state,min_soc,max_soc):
    current_state = round(300*intial_state,2) 
    min_level = round(300*min_soc,2)
    max_level = round(300*max_soc,2)
    battery_allocation = solar_gen - demand
    chargingStatus = getChargingStatus(battery_allocation)
    
    solar_excess = False
    solar_excess_energy = 0
    demand_shortage = False
    demand_shortage_amount = 0
    battery_usage = 0
    
    if chargingStatus == True:
        demand_shortage = False
        demand_shortage_amount = 0
        if current_state < max_level:
            chargingStatus = True
            remaininCharge = current_state + battery_allocation
            if remaininCharge >= max_level:
                #energy amount that used to charge the battery
                battery_usage = max_level - current_state
                solar_excess = True
                solar_excess_energy = battery_allocation - battery_usage
                remaininCharge = max_level
            else: #the latest charged amount is less than max level
                battery_usage = battery_allocation
                solar_excess = False
        else:
            chargingStatus = False
            battery_usage = 0
            solar_excess = True
            solar_excess_energy = battery_allocation
            remaininCharge = max_level
    # battery discharging
    else:
        solar_excess = False
        solar_excess_energy = 0
        if current_state >= min_level:
            chargingStatus = False
            remaininCharge = current_state + battery_allocation
            if remaininCharge <=min_level:
                battery_usage = current_state - min_level
                demand_shortage = True
                demand_shortage_amount = battery_allocation + battery_usage
                remaininCharge = min_level
            else:
                battery_usage = battery_allocation
                demand_shortage = False
                demand_shortage_amount = 0
                
        else:
            battery_usage = 0
            demand_shortage = True
            demand_shortage_amount = battery_allocation
            remaininCharge = min_level
                
    return solar_excess,solar_excess_energy,battery_usage,chargingStatus,remaininCharge,demand_shortage,demand_shortage_amount

init_stage = 0.6
for i in range(24):
    solar_excess,solar_excess_energy,battery_usage,chargingStatus,remaininCharge,demand_shortage,demand_shortage_amount = getBatteryAllocation(solar_generation_kw[i],demand[i],init_stage,0.2,0.96)
    print('solar gen:',solar_generation_kw[i])
    print('demand: ',demand[i])
    print('solar excess: ',solar_excess)
    print('solar_excess_energy: ',solar_excess_energy)
    print('battery_usage: ',battery_usage)
    print('chargingStatus: ',chargingStatus)
    print('remaininCharge: ',remaininCharge)
    print('demand_shortage: ',demand_shortage)
    print('demand_shortage_amount: ',demand_shortage_amount)
    init_stage = round(remaininCharge/300,2)
    print('init_stage:',init_stage)
    print('-------------------------------------')
    

