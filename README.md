# Bras Robotique 2DOF - Analyse et Animation

## Description
Ce projet est une simulation académique d’un bras robotique plan à 2 degrés de liberté (2DOF).  
Il permet de :

- Calculer la **cinématique directe** pour déterminer la position de l'effecteur en fonction des angles articulaires.
- Calculer la **matrice Jacobienne** et analyser les **singularités**.
- Animer le bras avec visualisation en temps réel de la trajectoire et des angles.
- Étudier l’espace de travail et la cinématique inverse (coude haut/coude bas).
- Comparer les caractéristiques avec un bras 3DOF.

Le projet est développé en **Python** et utilise des concepts de **robotique académique** et **cinématique différentielle**.

---
## Concepts utilisés

1. **CINÉMATIQUE DIRECTE (Forward Kinematics)**  
   - Permet de calculer la position de l’effecteur à partir des angles des articulations.  
   - Pour un bras 2DOF :  
     \[
     x_2 = L_1 \cos(\theta_1) + L_2 \cos(\theta_1 + \theta_2)
     \]  
     \[
     y_2 = L_1 \sin(\theta_1) + L_2 \sin(\theta_1 + \theta_2)
     \]

2. **JACOBIEN**  
   - Matrice 2x2 qui relie la vitesse des articulations à la vitesse linéaire de l’effecteur.  
   - Utile pour détecter les **singularités** et calculer les vitesses.

3. **SINGULARITÉS**  
   - Configurations où le bras perd un ou plusieurs degrés de liberté.  
   - Pour 2DOF, la singularité se produit quand sin(θ2) ≈ 0 (bras étendu ou replié).

4. **CINÉMATIQUE INVERSE (Inverse Kinematics)**  
   - Calcul des angles articulaires à partir d’une position cible.  
   - Pour un bras 2DOF, il existe deux solutions : **coude haut** et **coude bas**.

5. **ANIMATION ET VISUALISATION**  
   - Utilisation de `matplotlib` pour afficher le bras, les angles et la trajectoire de l’effecteur en temps réel.

---

### Exemple de Code

```py
import numpy as np

def cinematique_directe_2dof(theta1, theta2, L1=10, L2=7):
    t1 = np.radians(theta1)
    t2 = np.radians(theta2)
    x1 = L1 * np.cos(t1)
    y1 = L1 * np.sin(t1)
    x2 = x1 + L2 * np.cos(t1 + t2)
    y2 = y1 + L2 * np.sin(t1 + t2)
    return x1, y1, x2, y2

def calculer_jacobien_2dof(theta1, theta2, L1=10, L2=7):
    t1 = np.radians(theta1)
    t2 = np.radians(theta2)
    J = np.zeros((2,2))
    J[0,0] = -L1*np.sin(t1) - L2*np.sin(t1+t2)
    J[1,0] =  L1*np.cos(t1) + L2*np.cos(t1+t2)
    J[0,1] = -L2*np.sin(t1+t2)
    J[1,1] =  L2*np.cos(t1+t2)
```

---


**Lien vers le Dépôt GitHub :** [https://github.com/ElkhoulatiYahya/Bras_Robotique_2DOF]


