import numpy as np

def calculer_espace_travail(L1, L2):
    rayon_min = abs(L1 - L2)
    rayon_max = L1 + L2
    surface = np.pi * (rayon_max**2 - rayon_min**2)
    return rayon_min, rayon_max, surface
