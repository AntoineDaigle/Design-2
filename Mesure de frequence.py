import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.signal import savgol_filter
import pandas as pd
import os

"""Script permetant de lire l'oscillation de la lame en fonction du temps. Ajout d'un Curve_fit avec scipy pour obtenir le coefficient d'amortissement ainsi qu'un filtre maison.

Returns:
    int: Coefficient d'amortissement
    matplotlib : Graphique  de l'oscillation de la lame en fonction du temps
"""


if os.path.exists("Résultat prise mesure lame.txt"):
    os.remove("Résultat prise mesure lame.txt")
else:
    print("The file does not exist")



nb_de_set = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Set de données à traiter
Document = open("Résultat prise mesure lame.txt", "x")

ammor = []
freqosci = []

for _ in nb_de_set:
#################### Chercher le fichier

    if _ >= 10:
        position = r"Test capteur de position\Prise de mesure {}\F00{}CH1.CSV".format(_, _)
        df = pd.read_csv(position, index_col=False)
    else: 
        position = r"Test capteur de position\Prise de mesure {}\F000{}CH1.CSV".format(_, _)
        df = pd.read_csv(position, index_col=False)


    ################## Sommets des données

    # Première étape pour filtrer les données
    Peak = find_peaks(df["Tension"], distance=50)

    Temps_peak = []
    Tension_peak = []

    for i in Peak[0]:
        Temps_peak.append(df.iloc[i]["Temps"])
        Tension_peak.append(df.iloc[i]["Tension"])

    index = Tension_peak.index(max(Tension_peak))

    Temps_peak = Temps_peak[index:]
    Tension_peak = Tension_peak[index:]

    new_dataframe = df.iloc[Peak[0][index]:Peak[0][-1]]


    peak_fil = find_peaks(new_dataframe["Tension"], distance=50)

    # J'ai maintenant un nouveau data frame que je vais traiter

    new_ten= []
    new_tem = []

    for i in peak_fil[0]:
        new_ten.append(new_dataframe.iloc[i]["Tension"])
        new_tem.append(new_dataframe.iloc[i]["Temps"])



    ################## Curve_fit

    def func(Temps_peak, a, b, d):
        return a * np.exp(-b/Temps_peak) + d

    param, param_cova = curve_fit(func, new_tem, new_ten, maxfev=5000)

    ammor.append(param[1])



    ##################### Section calcul de la fréquence d'oscillation

    def frequence_osci(Temps, num_peak):
        """Déterminer la fréquence d'oscillation de la lame.

        Args:
            Temps (lst): Liste du temps ou les sommets sont situé
            num_peak (int): Nombre de peak souhaité

        Returns:
            int: Moyenne de la fréquence d'oscillation calculé avec les sommets.
        """
        temps = Temps[0:num_peak]
        w_0 = []

        for i in range(num_peak):
            if i == num_peak - 1:
                return freqosci.append(np.mean(w_0))

            else:
                w_0.append(1/(temps[i+1] - temps[i]))

    Nombre_sommets = 8  # Sélectionne le nombre de sommet pour le calcul

    freq_temps = new_tem[:Nombre_sommets]
    freq_tensi = new_ten[:Nombre_sommets]
    print(frequence_osci(new_tem, Nombre_sommets))
    




    ###################### Génération du graphique
    # fig, (ax1, ax2, ax3) = plt.subplots(3)
    # plt.suptitle("Données brutes et traitement des données de l'essai: {}".format(_))
    # ax1.plot(df["Temps"], df["Tension"], label="Données brutes")
    # ax3.plot(new_tem, new_ten, label="Sommets")
    # ax3.plot(new_dataframe["Temps"], func(new_dataframe["Temps"], *param), label="Curve_fit")
    # ax3.scatter(freq_temps, freq_tensi, color="red", label=r"Sommets utilisés pour $\omega_0$")
    # # ax2.plot(new_dataframe["Temps"], savgol_filter(new_dataframe["Don"], 51, 2), label="Données filtrées")
    # ax2.plot(new_dataframe["Temps"], savgol_filter(new_dataframe["Tension"], 51, 2), label="Données filtrées")
    # ax1.legend()
    # ax2.legend()
    # ax3.legend()
    # ax1.set(ylabel='Signal [V]')
    # ax2.set(ylabel="Signal [V]")
    # ax3.set(ylabel="Signal [V]", xlabel="Temps [s]")
    # # plt.savefig("Oscillation de la lame", dpi=600)    # Pour sauvegarder la figure, don't uncomment this fucking line if you don't want to save 3489 figures
    # plt.show()

fig, (ax1, ax2) = plt.subplots(2)
plt.suptitle("Résultat des simulations")
ax1.scatter(nb_de_set, ammor, label="Data")
ax1.axhline(np.mean(ammor), c="r", linestyle="--", label="moyenne")
ax1.set(ylabel="Coeff d'ammort")
ax2.scatter(nb_de_set, freqosci, label="Data")
ax2.axhline(np.mean(freqosci), c="r", linestyle="--", label="moyenne")
ax2.set(ylabel="Fréquence [Hz]", xlabel="Numéro de l'essai")
ax1.legend()
ax2.legend()
plt.show()

Document.write("-- Resultat du traitement des donnees --\n\n")

Document.write("La frequence d'oscillation pour les differentes simulations:\n")
for i in range(len(freqosci)):
    Document.write("\tTest {}: {} Hz\n".format(nb_de_set[i], round(freqosci[i], 4)))
Document.write("\n\nLe coefficient d'ammortissement pour les differentes simulations:\n")
for i in range(len(ammor)):
    Document.write("\tTest {}: {} \n".format(nb_de_set[i], round(ammor[i], 6)))
Document.write("\n\nLa frequence d'oscillation moyenne est de: {} Hz.\n".format(round(np.mean(freqosci), 4)))
Document.write("L'ecart-type de la frequence d'oscillation est de: {} Hz.\n\n".format(round(np.std(freqosci), 4)))
Document.write("Le coefficient d'ammortissement moyen est le suivant: {}.\n".format(round(np.mean(ammor), 4)))
Document.write("L'ecart-type du coefficient d'ammortissement est de: {}.".format(round(np.std(ammor), 4)))
Document.close()
print("SCRIPT COMPLÉTÉ")

#allo modification