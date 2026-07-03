# Use real, predicted data automatically, install requests on packages first
import requests
sunlight_perhour = []
household_demand = 0
panel_efficiency = 0
battery_capacity = 0
current_battcharge = 0

def fetch_sunlight():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=-6.9175&longitude=107.6191"
        "&hourly=shortwave_radiation"
        "&timezone=Asia%2FJakarta"
    )

    response = requests.get(url)
    data = response.json()
    if "hourly" not in data:
        print("API error:", data)
        return [0] * 24 # If API fails, sunlight is set to 0 so program doesn't crash

    return data["hourly"]["shortwave_radiation"][:24]
    
# Manual Input, use sunlight scale/sun irradiance
def setup_data():
    global sunlight_perhour, household_demand, panel_efficiency, battery_capacity, current_battcharge
    sunlight_perhour = []
    for i in range(24):
        value = int(input("Enter sunlight intensity in Watts during " + str(i) + ":00 : "))
        sunlight_perhour.append(value)
    print("Sum sunlight: ", sum(sunlight_perhour))
        
    household_demand = float(input("Enter household usage in kW per hour: "))
    panel_efficiency = float(input("Enter sunlight panel efficiency in decimal: ")) # Converts sunlight scale to kW output
    battery_capacity = float(input("Enter battery capacity in kW: "))
    current_battcharge = float(input("Enter current battery capacity in kW: ")) # Starting battery level

# Automated input, also uses sun irradiance
def automated_data():
    global sunlight_perhour, household_demand, panel_efficiency, battery_capacity, current_battcharge

    sunlight_perhour = fetch_sunlight()
    print("Sunlight data loaded:", sunlight_perhour)

    household_demand = float(input("Enter household usage in kW per hour: "))
    panel_efficiency = float(input("Enter sunlight panel efficiency in decimal: ")) # Converts sunlight scale to kW output
    battery_capacity = float(input("Enter battery capacity in kW: "))
    current_battcharge = float(input("Enter current battery charge in kW: ")) # Starting battery level

# Engine
def engine_loop():
    global current_battcharge, total_solar, total_waste, total_deficit_hours, final_status
    total_solar = 0
    total_deficit_hours = 0
    total_waste = 0
    for hour in range (24):
        # Calculate solar generation for this hour and total solar
        solar_generated = (sunlight_perhour[hour] / 1000) * panel_efficiency # Simplified solar model
        total_solar = total_solar + solar_generated
       # Find surplus/deficit
        net_energy = solar_generated - household_demand
        
        if net_energy > 0:
            # Excess power generated, so charge battery
            current_battcharge = current_battcharge + net_energy
            
            if current_battcharge > battery_capacity:
                waste = current_battcharge - battery_capacity
                total_waste = total_waste + waste
                current_battcharge = battery_capacity
        else:
            # Energy deficit, so draw from battery
            current_battcharge = current_battcharge + net_energy # Net energy is negative
            total_deficit_hours = total_deficit_hours + 1

            if current_battcharge < 0:
                current_battcharge = 0
                
    if current_battcharge >= battery_capacity:
        final_status = "Battery Full"
    elif current_battcharge == 0:
        final_status = "Battery Empty"
    else:
        final_status = "Battery Partially Charged"


choice = int(input("Would you like to use manual (1) or live data (2)?: "))

if choice == 1:
    setup_data()

elif choice == 2:
    automated_data()
    
else:
    print("Input not accepted")
    exit()
    
engine_loop()

print("\n =====Final Results=====")
print("Total solar generated: ", total_solar, " kW" )
print("Final Battery Charge: ", current_battcharge, " kW")
print("Total Wasted Energy: ", total_waste, " kW")
print("Total Deficit Hours: ", total_deficit_hours)
print("Final Status: ", final_status)
