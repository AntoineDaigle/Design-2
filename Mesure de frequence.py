import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.signal import butter
from scipy.signal import sosfilt
import pandas as pd
import os

"""Script permetant de lire l'oscillation de la lame en fonction du temps. Ajout d'un Curve_fit avec scipy pour obtenir le coefficient d'amortissement.

Returns:
    int: Coefficient d'amortissement 
    matplotlib : Graphique  de l'oscillation de la lame en fonction du temps
"""


if os.path.exists("Résultat prise mesure lame.txt"):
    os.remove("Résultat prise mesure lame.txt")
else:
    print("The file does not exist")

nb_de_set = [1, 2]
Document = open("Résultat prise mesure lame.txt", "x")

ammor = []
freqosci = []

for _ in nb_de_set:
#################### Chercher le fichier

    position = r"Test capteur de position\Prise de mesure {}\F000{}CH1.CSV".format(_, _)
    df = pd.read_csv(position, index_col=False)
    plt.plot(df["Temps"], df["Tension"], label="Données brutes")

    # print(df.head())  # Pour voir la forme du CSV:



    ##################### Tentative de filtre
    # sos = butter(5, 4) #aquisition en milliseconde
    # filtered = sosfilt(sos, df["Tension"])






    ################## Sommets des données

    Peak = find_peaks(df["Tension"], distance=50)

    Temps_peak = []
    Tension_peak = []

    for i in Peak[0]:
        Temps_peak.append(df["Temps"][i])
        Tension_peak.append(df["Tension"][i])








    ################## Curve_fit

    index = Tension_peak.index(max(Tension_peak))

    Temps_peak = Temps_peak[index:]
    Tension_peak = Tension_peak[index:]

    def func(Temps_peak, a, b, d):
        return a * np.exp(-b/Temps_peak) + d

    param, param_cova = curve_fit(func, Temps_peak, Tension_peak, maxfev=5000)
    # print("Les paramètres sont calculés, l'ammortissement est de: {}".format(param[1])) # Uncomment for result
    ammor.append(param[1])

    plt.plot(Temps_peak, func(Temps_peak, *param), label="Curve_fit")
    plt.plot(Temps_peak, Tension_peak, label="Sommet")




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
                # return "La fréquence d'oscillation est de: {} Hz".format(np.mean(w_0)) #Uncomment for result
                
            else:
                w_0.append(1/(temps[i+1] - temps[i]))

    Nombre_sommets = 8  # Sélectionne le nombre de sommet pour le calcul

    freq_temps = Temps_peak[:Nombre_sommets]
    freq_tensi = Tension_peak[:Nombre_sommets]
    print(frequence_osci(Temps_peak, Nombre_sommets))
    plt.scatter(freq_temps, freq_tensi, color="red", label=r"Sommets utilisés pour $\omega_0$")





    ###################### Génération du graphique

    plt.legend()
    plt.xlabel("Temps [s]")
    plt.ylabel("Signal [V]")
    plt.title("Set de données de l'essai: {}".format(_))
    # plt.savefig("Oscillation de la lame", dpi=600)    # Pour sauvegarder la figure, don't uncomment this fucking line if you don't want to save 3489 figures
    # plt.show()

Document.write("-- Resultat du traitement des donnees --\n\n")

Document.write("La frequence d'oscillation pour les differentes simulations:\n")
for i in range(len(freqosci)):
    Document.write("    Test {}: {} Hz\n".format(i + 1, freqosci[i]))
Document.write("\n\nLe coefficient d'ammortissement pour les differentes simulations:\n")
for i in range(len(ammor)):
    Document.write("    Test {}: {} \n".format(i + 1, ammor[i]))
Document.write("\n\nLa frequence d'oscillation moyenne est de: {} Hz.\n".format(np.mean(freqosci)))
Document.write("L'ecart-type de la frequence d'oscillation est de: {} Hz.\n\n".format(np.std(freqosci)))
Document.write("Le coefficient d'ammortissement moyen est le suivant: {}.\n".format(np.mean(ammor)))
Document.write("L'ecart-type du coefficient d'ammortissement est de: {}.".format(np.std(ammor)))
Document.close()
print("SCRIPT COMPLÉTÉ")