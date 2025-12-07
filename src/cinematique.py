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
    return J

def detecter_singularites_2dof(theta1, theta2, L1=10, L2=7):
    J = calculer_jacobien_2dof(theta1, theta2, L1, L2)
    det_J = np.linalg.det(J)
    t2 = np.radians(theta2)
    is_singular = (abs(det_J) < 0.01) or (abs(np.sin(t2)) < 0.01)
    return is_singular, det_J

def calculer_vitesse_effecteur_2dof(theta1, theta2, dtheta1, dtheta2, L1=10, L2=7):
    J = calculer_jacobien_2dof(theta1, theta2, L1, L2)
    dtheta_rad = np.radians([dtheta1, dtheta2])
    vitesse = J @ dtheta_rad
    return vitesse[0], vitesse[1]

def cinematique_inverse_2dof(x, y, L1=10, L2=7):
    d = np.sqrt(x**2 + y**2)
    if d > (L1 + L2) or d < abs(L1 - L2):
        return None, None
    cos_theta2 = max(-1, min(1, (d**2 - L1**2 - L2**2)/(2*L1*L2)))
    theta2_1 = np.degrees(np.arccos(cos_theta2))
    theta2_2 = -theta2_1
    alpha = np.degrees(np.arctan2(y,x))
    cos_beta = max(-1, min(1, (L1**2 + d**2 - L2**2)/(2*L1*d)))
    beta = np.degrees(np.arccos(cos_beta))
    theta1_1 = alpha - beta
    theta1_2 = alpha + beta
    return (theta1_1, theta2_1), (theta1_2, theta2_2)
