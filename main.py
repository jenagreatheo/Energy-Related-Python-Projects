# This project was ran on Wokwi, Link to project: https://wokwi.com/projects/468521085279259649
import time
import machine

# Setting up Inputs, Constants and Outputs
solar_ADC = machine.ADC(26) # Used to read solar intensity
gLED = machine.Pin(14, machine.Pin.OUT)
rLED = machine.Pin(13, machine.Pin.OUT)
alarm = machine.PWM(machine.Pin(15))
max_ADC = 65535
volts = 12.0 # Simulate 12 volts

def track_power(raw_sunlight):
    sunlight_efficiency = raw_sunlight / max_ADC
    current = sunlight_efficiency * 5.0 # Simulate max current as 5 A
    power = current * volts # Calculate power using P = VI
    return current, power

while True:
    raw_sunlight = solar_ADC.read_u16()
    current, power = track_power(raw_sunlight)
    sun_level_percent = (raw_sunlight/max_ADC)*100
    print("Sunlight Level %: ", str(sun_level_percent))
    print("Output Current: ", str(current))
    print("Total Power: ", str(power))

    if power < 15.0:
        # Not enough power, display warning
        gLED.value(0)
        rLED.value(1)
        alarm.freq(300)
        print("Energy Deficit Detected")

    elif power > 55.0:
        # Too much power, display warning
        gLED.value(1)
        rLED.value(1) # Making it orange/yellow
        alarm.freq(600)
        print("Energy Overload detected")

    else:
        # Power is optimal
        gLED.value(1)
        rLED.value(0)
        print("Optimal Energy Detected")

    time.sleep(5) # Waits 1 second before checking again
