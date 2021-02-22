import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
import pandas as pd


position = r"C:\Users\antoi\Desktop\testest.csv"
df = pd.read_csv(position, index_col=False)

#Pour voir la forme du CSV:
#print(df.head())

Peak = find_peaks(df["Tension"], distance=50)
#print(Peak[0])

Temps_peak = []
Tension_peak = []

for i in Peak[0]:
    Temps_peak.append(df["Temps"][i])
    Tension_peak.append(df["Tension"][i])

plt.plot(df["Temps"], df["Tension"])
plt.plot(Temps_peak, Tension_peak)
plt.show()

