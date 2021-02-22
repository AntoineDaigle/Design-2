import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.signal import butter
from scipy.signal import sosfilt
import pandas as pd


position = r"C:\Users\antoi\Desktop\testest.csv"
df = pd.read_csv(position, index_col=False)

#Pour voir la forme du CSV:
#print(df.head())

# sos = butter(5, 4) #aquisition en milliseconde
# filtered = sosfilt(sos, df["Tension"])


Peak = find_peaks(df["Tension"], distance=50)

Temps_peak = []
Tension_peak = []


for i in Peak[0]:
    Temps_peak.append(df["Temps"][i])
    Tension_peak.append(df["Tension"][i])

#Maxi du peak
Maxi = df.loc[df['Tension'].idxmax()]
print(Maxi)


def func(Temps_peak, a, b, d):
    return a * np.exp(-b/Temps_peak) + d

param, param_cova = curve_fit(func, Temps_peak, Tension_peak)

print("Les paramètres sont calculés, l'ammortissement est de: {}".format(param[1]))

plt.plot(df["Temps"], df["Tension"], label="Données brutes")
plt.plot(Temps_peak, Tension_peak, label="Sommet")
plt.plot(Temps_peak, func(Temps_peak, *param), label="Curve_fit")
plt.legend()
plt.show()

