class GeneralPriceAlgorithm:
    def __init__(self,demand,supply,isDemSupMatch,battery_allocation,batteryCharging,battery_dischargig,solar_surplus):
        self.demand = demand #demand value
        self.suppply = supply # supply values
        self.battery_allocation = battery_allocation #battery allcation value can be negative or positive
        self.batery_charging = batteryCharging # boolean value 
        self.solar_surplus = solar_surplus # 
        self.isDemSupMatch = isDemSupMatch # boolean value 
        self.battery_discharging = battery_dischargig #boolean value
        self.max_price = 100
        self.min_price = 10
        self.serviceChargePerUnit = 0.01
        self.diesel_cost = 30
        
    def calculatePrice(self,solar_unit_cost,battery_unit_cost,demandFactor):
        # Case 1: demand = supply
        if (self.isDemSupMatch and not self.solar_surplus):
            print('Demand equal supply')
            market_price = (self.suppply * solar_unit_cost + self.serviceChargePerUnit * self.demand) / self.demand
            
        # Case 2: if demand > gen and battery used to fill the energy
        elif (self.isDemSupMatch and self.battery_discharging):
            generationCost = self.suppply * solar_unit_cost
            serviceCharge = self.serviceChargePerUnit * self.demand
            batteryCost = (self.battery_allocation * battery_unit_cost) * (1 + demandFactor * ((S_max - soc) / s_max))
            calculated_price = (generationCost + serviceCharge + batteryCost) / self.demand
            market_price = min(self.max_price,calculated_price)
            print('Demand > gen and battery is used to fill the energy')
        
        # Case 3: if demand > gen and price used to fill the energy or diesel gene is used
        elif (not self.isDemSupMatch and not self.battery_discharging):
            excess_demand = self.demand - self.suppply
            base_price = (self.suppply* solar_unit_cost + excess_demand * self.diesel_cost) / self.demand
            calculated_price = base_price * (1 + demandFactor * (excess_demand / self.suppply))
            market_price = min(self.max_price, calculated_price)
            print('Demand > gen and diesel generator is used to fill the demand')
            
        # Case 4: solar > demand and have surplus and charge the battery, no solar surplus
        elif (self.isDemSupMatch and self.batery_charging and not self.solar_surplus):
            market_price = (self.suppply* solar_unit_cost + self.serviceChargePerUnit * self.demand) / self.demand
            print('gen > demand and battery is chared')
            
        # Case 5: solar > demand and and charged the battery and have solar surplus
        elif (self.isDemSupMatch and self.solar_surplus and self.batery_charging):
            effective_solar_generation = self.suppply - self.battery_allocation
            excess_solar = effective_solar_generation - self.demand
            base_price = (effective_solar_generation * solar_unit_cost + self.serviceChargePerUnit * self.demand) / self.demand
            calculated_price = base_price * (1 - demandFactor * (excess_solar / effective_solar_generation))
            market_price = max(self.min_price, calculated_price)
            print('Gen > demand and battery is charged then reduce the price due to excess solar')
            
        # Case 6: Solar > Demand, battery fully charged, and solar surplus
        elif self.isDemSupMatch and self.solar_surplus and not self.battery_charging:
            excess_solar = self.suppply - self.demand
            base_price = (self.suppply * solar_unit_cost + self.serviceChargePerUnit * self.demand) / self.demand
            calculated_price = base_price * (1 - demandFactor * (excess_solar / self.suppply))
            market_price = max(self.min_price, calculated_price)
            print('Demand > gen and battery is used to fully charged.Then reduce the price')
            
        return market_price
            
            
                        
new = GeneralPriceAlgorithm(demand=40,supply=60,isDemSupMatch=True,battery_allocation=20,batteryCharging=True,battery_dischargig=False,solar_surplus=True)
print(new.calculatePrice(20,10,0.2))
    
    