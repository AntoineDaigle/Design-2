# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 17:03:08 2021

@author: antoi
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


class modélisation_poutre():
    """Classe générant le mode fondamentale de la poutre
    """
    def __init__(self, longueur=0.3, largeur=0.05, epaisseur=0.001, Young=2.7*10**11, load=-2, poid=-0.1):
        """Initialise les variables utilisés pour la résolution

        Args:\n
            longueur (int): Longueur de la lame en mètre.\n
            largeur (int): Largeur de la lame en mètre.\n
            epaisseur (int): Épaisseur de la lame en mètre.\n
            Young (int): Module de Young de la lame en pascal.\n
            load (int): Charge sur la lame, doit être négatif pour bien simuler notre situation.\n
            poid (int): Poid de la lame
        """
        self.longueur = longueur
        self.largeur = largeur
        self.epaisseur = epaisseur
        self.young = Young
        self.load = load
        self.poid = poid

        
        self.I = (1/12) * self.epaisseur**3 * self.largeur
        self.a = self.longueur/2 #Position de la charge au milieu de la poutre

        #Équation de déflection
        self.x = np.linspace(0, self.longueur)
        self.y1 = (self.load * self.x**2)/(6*self.young * self.I) * (3*self.a - self.x)  #Charge milieu de la poutre
        self.y2 = (self.load * self.x**2)/(6*self.young * self.I) * (3*self.longueur - self.x)  #Charge au bout de la poutre
        self.y3 = (self.poid * self.x**2)/(24 * self.young * self.I) * (self.x**2 + 6 * self.poid**2 - 4 * self.poid * self.x)  #Charge répartie uniformément sur poutre


        #Déflexion maximale
        self.Def_max_y1 = round((self.load * self.longueur**3)/(3 * self.young * self.I), 5)
        self.Def_max_y2 = round((self.load * self.a**2)/(6*self.young * self.I) * (3*self.longueur - self.a), 5)
        self.Def_max_y3 = round((self.poid * self.longueur)/(8*self.young * self.I), 5)
        
    def Show_Deflection(self):
        """Montre le graphique du mode principal.
        """

        plt.plot(self.x, self.y1, label="Charge au milieu de la poutre")
        plt.plot(self.x, self.y2, label="Charge au bout de la poutre")
        plt.plot(self.x, self.y3, label="Charge répartie uniformément sur la poutre")
        plt.axhline(color="black")

        plt.grid()
        plt.legend()
        plt.title("Déflection de la poutre")
        plt.ylabel("hauteur de la déflection")
        plt.xlabel("Longueur de la lame")
        plt.show()

    def Max_Deflection(self):
        """Montre le maximum de déflexion possible de la lame.
        """
        print("Le maximum de déflection des poutres:")
        print("Charge au bout de la lame: {} mètre.".format(self.Def_max_y1))
        print("Charge au milieu de la lame: {} mètre.".format(self.Def_max_y2))
        print("Charge répartie uniformément sur la lame: {}".format(self.Def_max_y3))

    def Charge_Milieu_Poutre(self):
        
        #approx linéaire
        def func(x, a, b):
            return a * x + b

        param, param_cova = curve_fit(func, self.x, self.y1)
        print("Les paramètres linéaires sont:", param)

        #Approx Quadratique
        def func_quad(x, a, b, c):
            return a * x**2 + b*x + c
        
        param_quad, param_quad_cova = curve_fit(func_quad, self.x, self.y1)
        print("Les paramètres selon une quadratique sont:", param_quad)

        #Graphique
        plt.plot(self.x, self.y1, label="Masse au milieu de la lame")
        plt.plot(self.x, func(self.x, param[0], param[1]), "r+", label="Linéaire")

        plt.plot(self.x, func_quad(self.x, param_quad[0], param_quad[1], param_quad[2]), "y.", label="Approx quadratique")

        plt.grid()
        plt.axhline(color="black")
        plt.title("Tentative pour avoir fonction logique pour une masse au milieu de la poutre")
        plt.xlabel("Longeur de la lame")
        plt.ylabel("Déflection de la lame")
        plt.legend()
        plt.show()

    def Ideal_Beam(self):
        """Fonction qui montre la poutre avec se propre masse, sans sa propre masse et avec la correction linéaire.
        """
        Ideal = self.y1
        Ideal_approx = (self.load * self.a**2)/(6*self.young * self.I) * (3*self.x - self.a)

        Ideal_mass_beam = self.y1 + self.y3
        Ideal_mass_beam_approx = (self.load * self.a**2)/(6*self.young * self.I) * (3*self.x - self.a) + self.y3

        plt.plot(self.x, Ideal, "r--", label="Poutre Idéale")
        plt.plot(self.x, Ideal_approx, "r", label="Approx Poutre idéale")
        plt.plot(self.x, Ideal_mass_beam, "b--", label="Poutre idéale avec masse")
        plt.plot(self.x, Ideal_mass_beam_approx, "b", label="Approx Poutre idéale avec masse")
        plt.grid()
        plt.legend()
        plt.xlabel("Longueur [m]")
        plt.ylabel("Déflection [m]")
        plt.title("Flection de la poutre selon différent modèle")
        plt.show()


result = modélisation_poutre()
# print(result.Show_Deflection())
# print(result.Max_Deflection())
# print(result.Charge_Milieu_Poutre())
print(result.Ideal_Beam())
