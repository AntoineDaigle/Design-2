import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.signal import butter
from scipy.signal import sosfilt
import pandas as pd


position = r"Test capteur de position\Prise de mesure 1\F0001CH1.CSV"
df = pd.read_csv(position, index_col=False)




Peak = find_peaks(df["Tension"], distance=50)

Temps_peak = []
Tension_peak = []

for i in Peak[0]:
    Temps_peak.append(df["Temps"][i])
    Tension_peak.append(df["Tension"][i])

index = Tension_peak.index(max(Tension_peak))

Temps_peak = Temps_peak[index:]
Tension_peak = Tension_peak[index:]

new_dataframe = df.iloc[Peak[0][index]:Peak[0][-1]]


def func_sin(x, a, b, c, d):
    return a * np.sin(b*x + c) + d

parame, parame_co = curve_fit(func_sin, new_dataframe["Temps"][-250:], new_dataframe["Tension"][-250:])

Données_filtrées = new_dataframe["Tension"] - func_sin(new_dataframe["Temps"], *parame)


def func(Temps_peak, a, b, d):
    return a * np.exp(-b/Temps_peak) + d

param, param_cova = curve_fit(func, new_dataframe["Temps"], Données_filtrées, maxfev=5000)




plt.plot(df["Temps"], df["Tension"], label="Données brutes")
plt.plot(new_dataframe["Temps"], func_sin(new_dataframe["Temps"], *parame), label="Sinus")
plt.plot(new_dataframe["Temps"], func(new_dataframe["Temps"], *param), label="est")
plt.plot(new_dataframe["Temps"], Données_filtrées, label="Données filtrées")
plt.legend()
plt.show()