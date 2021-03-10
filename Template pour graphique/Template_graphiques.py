"""Template pour générer des graphiques à partir de colonnes Excel, de CSV ou de fichiers txt."""
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

#Remplacer ici par le path complet de votre fichier CSV. 
path = r"C:\Users\Famille Gougeon\Documents\GitHub\Design-2\Test capteur de position\Prise de mesure 0\F0000CH1.CSV"

A = ([], [])
#Ajouter des listes vides "y" si plusieurs courbes sont à mettre dans le même graphique

""" POUR UN CSV D'OSCILLOSCOPE
Ajouter ceci en tant que première ligne du CSV pour nommer les colonnes: ",,,x,y," (seulement l'intérieur des guillemets).
Habituellement, pour l'oscilloscope, ce sera ",,,temps,tension,". Le template est fait avec x et y
pour montrer le principe."""
if path[-3:] == "CSV":
    df = pd.read_csv(path, index_col=False)
    for i in range(len(df)):
        A[0].append(df["x"][i])
        A[1].append(df["y"][i])
        #A[2].append(df["y2"][i])
        #Et changer la première ligne du CSV pour ",,,x,y,y2,"
    plt.plot(A[0], A[1], color="b")
    #Vos titres d'axes
    plt.xlabel("Temps [s]")
    plt.ylabel("Tension [V]")
    plt.show()

"""POUR UN FICHIER TXT EN COLONNES DONT LA PREMIÈRE EST L'ABSCISSE"""
if path[-3:] == "txt":
    f = open(path, "r")
    lines = f.readlines()
    result = []
    for a in lines:
        result.append(a.replace("\n", "").replace(",", ".").split("\t"))
    for a in result:
        A[0].append(float(a[0]))
        A[1].append(float(a[1])) 
        #A[2].append(float(a[2]))
    f.close()
    plt.plot(A[0], A[1], color="b")
    #Vos titres d'axes
    plt.xlabel("Temps [s]")
    plt.ylabel("Tension [V]")
    plt.show()

"""POUR UN FICHIER EXCEL EN COLONNES NOMMÉES "X" ET "Y" (à la première rangée)"""
if path[-4:] == "xlsx":
    df = pd.read_excel(path, index_col=False)
    for i in range(len(df)):
        A[0].append(df["X"][i])
        A[1].append(df["Y"][i])
        #A[2].append(df["Y2"][i]))
    plt.plot(A[0], A[1], color="b")
    #Vos titres d'axes
    plt.xlabel("Temps [s]")
    plt.ylabel("Tension [V]")
    plt.show()

else:
    print("path ou extension invalide")
    