import pandas as pd
import numpy as np


nb_de_set = [-2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Set de données à traiter



position = r"C:\Users\Famille Gougeon\Documents\GitHub\Design-2\Test capteur de position\Prise de mesure {}\F000{}CH1.CSV".format(0, 0)
df = pd.read_csv(position, index_col=False)

A = ([], [])
for i in range(len(df)):
    A[0].append(df["Temps"][i])
    A[1].append(df["Tension"][i])
    
stringA0 = str(A[0])
stringA1 = str(A[1])
temps0 = open("temps0.txt", "w")
temps0.write(stringA0.replace("[", "").replace("]", "").replace(", ", "\n"))
tension0 = open("tension0.txt", "w")
tension0.write(stringA1.replace("[", "").replace("]", "").replace(", ", "\n"))
