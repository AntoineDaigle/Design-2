"""Module de Young - Design 2"""
import numpy as np

"Données en unités du SI [m, kg]"
Lame = {"L": 24*10**(-2), "B": 7.4*10**(-2), "H": 1/16*2.54*10**(-2), "masse": 67.25*10**(-3)}

"Fréquence d'oscillation mesurée [Hz]"
f = 15

I = Lame["B"]*Lame["H"]**3 / 12
Rn = 1.875
mu = Lame["masse"]/(30.1*10**(-2))
wn = 2*np.pi*f

"Module de Young"
E = (mu*wn**2 / I)*(Lame["L"]/Rn)**4
print(E)
