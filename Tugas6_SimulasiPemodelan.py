import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the temperature model for the tank
def tank_temp(Temp, time, P_heater, loss_coeff, c_p, rho, V, ambient_temp):
    # Calculate the rate of change of temperature
    dTemp_dt = (P_heater - loss_coeff * (Temp - ambient_temp)) / (rho * V * c_p)
    return dTemp_dt

# Simulation parameters
P_heater_full = 5000  # Full power of the heater in Watts (W)
loss_coeff = 10  # Heat loss coefficient (W/°C)
c_p = 4181  # Specific heat of water (J/kg°C)
rho = 1000  # Density of water (kg/m³)
V = 0.5     # Volume of water in the tank (m³)
ambient_temp = 25  # Ambient temperature (°C)

# Initial condition
Temp0 = 25  # Initial temperature of the water in the tank (°C)

# Time span for the simulation
time = np.linspace(0, 1800, 300)  # Simulate for 30 minutes (1800 seconds) with 300 points

# Define heater power over time
P_heater = np.ones(len(time)) * P_heater_full
P_heater[(time >= 15 * 60) & (time < 20 * 60)] = 0  # Heater is off from 15 to 20 minutes

# Simulate temperature change over time
Temp = np.zeros(len(time))
Temp[0] = Temp0  # Set initial temperature

# Run simulation
for i in range(1, len(time)):
    # Calculate temperature with current heater power
    Temp[i] = odeint(tank_temp, Temp[i-1], [time[i-1], time[i]], 
                     args=(P_heater[i], loss_coeff, c_p, rho, V, ambient_temp))[-1]

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(time / 60, Temp, 'b-', label="Temperatur air dalam tangki")
plt.axhline(y=ambient_temp, color='r', linestyle='--', label="Suhu Ruang")
plt.xlabel("Time (minutes)")
plt.ylabel("Temperature (°C)")
plt.title("Simulasi Kenaikan Suhu")
plt.legend()
plt.grid()
plt.show()
