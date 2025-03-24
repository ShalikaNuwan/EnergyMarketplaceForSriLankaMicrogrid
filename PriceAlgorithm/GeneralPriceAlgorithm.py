class GeneralPriceAlgorithm:
    def __init__(self,demand,supply,isDemSupMatch,battery_allocation,batteryCharging,battery_dischargig,solar_surplus):
        self.demand = demand
        self.suppply = supply
        self.battery_allocation = battery_allocation
        self.batery_charging = batteryCharging
        self.solar_surplus = solar_surplus
        self.isDemSupMatch = isDemSupMatch
        self.battery_discharging = battery_dischargig
        
    def calculatePrice(self,solar_cost,battery_cost,max_price):
        if (self.isDemSupMatch == True):
            # max (totalDemand * market_price - energyGen * solar_cost)
            pass
        # if demand > gen and battery used to fill the energy
        elif ((self.isDemSupMatch == True) and (self.battery_discharging == True)):
            # max (totalDemand * market_price - energyGen * solar_cost - battery usage * battery cost)
            pass
        # if demand > gen and price used to fill the energy
        elif ((self.isDemSupMatch == True) and (self.battery_discharging == False)):
            # max (totalDemand * market_price - energyGen * solar_cost - value of loss load)
            if (price > max_price):
                # max (totalDemand * market_price - energyGen * solar_cost - price for generator)
                pass
            pass
        
        # solar > demand and have surplus and charge the battery, no solar surplus
        elif ((self.isDemSupMatch == True) and (self.batery_charging == True) and (self.solar_surplus == False)):
            # max (totalDemand * market_price - energyGenUsed by customer * solar_cost)
            pass
        # solar > demand and and charged the battery and have solar surplus
        elif ((self.solar_surplus == True) and (self.batery_charging == True) and (self.solar_surplus == True)):
            
            pass
        
            
            
            
            
            
    
    


new = GeneralPriceAlgorithm(10,24,True,True,133)
new.calculatePrice(10,20)
    
    