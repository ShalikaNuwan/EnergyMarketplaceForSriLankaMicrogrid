class GeneralPriceAlgorithm:
    def __init__(self, demand, supply, isDemSupMatch, battery_allocation, battery_charging, battery_discharging, solar_surplus):
        self.demand = demand
        self.supply = supply  # Fixed spelling
        self.battery_allocation = battery_allocation
        self.battery_charging = battery_charging  # Fixed spelling
        self.solar_surplus = solar_surplus
        self.isDemSupMatch = isDemSupMatch
        self.battery_discharging = battery_discharging  # Fixed spelling
        
    def calculatePrice(self, solar_of_hour, battery_cost, max_price, min_price, surcharge, demand_of_hour, unitCostSolar, demand_factor, diesel_cost, S_max, soc, s_max):
        
        # Case 1: Demand == Generation
        if self.isDemSupMatch and not self.solar_surplus:
            market_price = (solar_of_hour * unitCostSolar + surcharge * demand_of_hour) / demand_of_hour
        
        # Case 2: Demand > Generation and battery is discharging
        elif self.isDemSupMatch and self.battery_discharging:
            generationCost = solar_of_hour * unitCostSolar
            demandCost = surcharge * demand_of_hour
            batteryCost = ((self.battery_allocation) * unitCostSolar) * (1 + demand_factor * ((S_max - soc) / s_max))
            market_price = (generationCost + demandCost + batteryCost) / demand_of_hour
             
        # Case 3: Demand > Generation and no battery usage (diesel required)
        elif self.isDemSupMatch and not self.battery_discharging:
            excess_demand = demand_of_hour - solar_of_hour
            base_price = (solar_of_hour * unitCostSolar + excess_demand * diesel_cost) / demand_of_hour
            calculated_price = base_price * (1 + demand_factor * (excess_demand / solar_of_hour))
            market_price = min(max_price, calculated_price)
            
        # Case 4: Solar == Demand + Battery Charging
        elif self.isDemSupMatch and self.battery_charging and not self.solar_surplus:
            market_price = (solar_of_hour * unitCostSolar + surcharge * demand_of_hour) / demand_of_hour
            
        # Case 5: Solar > Demand, charging battery, and solar surplus
        elif self.isDemSupMatch and self.solar_surplus and self.battery_charging:
            effective_solar_generation = solar_of_hour - self.battery_allocation
            excess_solar = effective_solar_generation - demand_of_hour
            base_price = (effective_solar_generation * unitCostSolar + surcharge * demand_of_hour) / demand_of_hour
            calculated_price = base_price * (1 - demand_factor * (excess_solar / effective_solar_generation))
            market_price = max(min_price, calculated_price)
            
        # Case 6: Solar > Demand, battery fully charged, and solar surplus
        elif self.isDemSupMatch and self.solar_surplus and not self.battery_charging:
            excess_solar = solar_of_hour - demand_of_hour
            base_price = (solar_of_hour * unitCostSolar + surcharge * demand_of_hour) / demand_of_hour
            calculated_price = base_price * (1 - demand_factor * (excess_solar / solar_of_hour))
            market_price = max(min_price, calculated_price)

        else:
            market_price = min_price  # Default fallback

        return market_price  # Added return statement

# Example usage:
new = GeneralPriceAlgorithm(10, 24, True, 5, True, False, False)
price = new.calculatePrice(
    solar_of_hour=10, battery_cost=20, max_price=100, min_price=10, surcharge=5, 
    demand_of_hour=15, unitCostSolar=0.2, demand_factor=0.1, diesel_cost=0.3, 
    S_max=100, soc=50, s_max=100
)
print(f"Market Price: {price}")
