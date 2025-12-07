import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, display
from cinematique import cinematique_directe_2dof, calculer_jacobien_2dof, calculer_vitesse_effecteur_2dof, detecter_singularites_2dof

def lancer_animation_2dof(L1=10, L2=7):
    fig, axes = plt.subplots(1, 3, figsize=(18,5))
    print("Animation 2DOF avec calculs de cinematique en temps reel")
    #Création d'une nouvelle figure pour l'animation avec 3 sous-graphiques côte à côte
    fig_anim, axes_anim = plt.subplots(1, 3, figsize=(18, 5))

    #----------------------------------------------------------------------------
    #Configuration du premier axe : vue du bras
    #----------------------------------------------------------------------------
    axes_anim[0].set_xlim(-20, 20)
    axes_anim[0].set_ylim(-20, 20)
    axes_anim[0].set_aspect('equal')
    axes_anim[0].grid(True, alpha=0.3)
    axes_anim[0].set_title("Animation du bras 2DOF", fontsize=12, fontweight='bold')
    axes_anim[0].set_xlabel("Position X (cm)")
    axes_anim[0].set_ylabel("Position Y (cm)")

    #----------------------------------------------------------------------------
    #Configuration du deuxième axe : évolution des angles dans le temps
    #----------------------------------------------------------------------------
    axes_anim[1].set_xlim(0, 360)
    axes_anim[1].set_ylim(-180, 180)
    axes_anim[1].grid(True, alpha=0.3)
    axes_anim[1].set_title("Évolution des angles", fontsize=12, fontweight='bold')
    axes_anim[1].set_xlabel("Frame")
    axes_anim[1].set_ylabel("Angle (degrés)")
    axes_anim[1].axhline(y=0, color='k', linestyle='-', alpha=0.3)

    #----------------------------------------------------------------------------
    #Configuration du troisième axe : informations textuelles
    #----------------------------------------------------------------------------
    axes_anim[2].axis('off')  #Désactive les axes pour afficher du texte
    #Création d'un objet texte qui sera mis à jour à chaque frame
    info_text_obj = axes_anim[2].text(0.05, 0.5, '', fontfamily='monospace', fontsize=9,
                                    verticalalignment='center',
                                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

    #----------------------------------------------------------------------------
    #Création des objets graphiques qui seront animés
    #----------------------------------------------------------------------------
    #Ligne représentant le bras
    line_anim, = axes_anim[0].plot([], [], marker='o', linewidth=2, markersize=8, color='blue')
    #Trajectoire de l'effecteur (ligne pointillée verte)
    trajectory_anim, = axes_anim[0].plot([], [], 'g--', alpha=0.5, linewidth=1)
    #Point représentant l'effecteur
    effecteur_dot_anim, = axes_anim[0].plot([], [], 'go', markersize=10, alpha=0.7)

    #Lignes pour l'historique des angles
    angle1_line_anim, = axes_anim[1].plot([], [], 'r-', label='θ1', linewidth=2)
    angle2_line_anim, = axes_anim[1].plot([], [], 'orange', label='θ2', linewidth=2)
    angle_total_line_anim, = axes_anim[1].plot([], [], 'g-', label='θ1+θ2', linewidth=2, alpha=0.5)
    axes_anim[1].legend()  #Ajout de la légende pour identifier les courbes

    #----------------------------------------------------------------------------
    #Variables pour stocker l'historique des positions et angles
    #----------------------------------------------------------------------------
    x_history_anim = []  #Historique des positions X de l'effecteur
    y_history_anim = []  #Historique des positions Y de l'effecteur
    theta1_history_anim = []  #Historique de l'angle θ1
    theta2_history_anim = []  #Historique de l'angle θ2
    theta_total_history_anim = []  #Historique de l'angle total
    frame_history_anim = []   #Historique des numéros de frame

    #----------------------------------------------------------------------------
    #Définition de la fonction de mise à jour appelée à chaque frame
    #----------------------------------------------------------------------------
    def update_animation(frame):

        #------------------------------------------------------------------------
        #1.Calcul des nouveaux angles pour cette frame
        #------------------------------------------------------------------------
        #Chaque angle suit une loi de variation différente pour créer
        #Un mouvement intéressant et montrer différentes configurations
        
        #θ1 varie sinusoïdalement avec une amplitude de 180° et une fréquence de 0.5
        #La formule : 90 * sin(0.5*frame) + 90 donne des valeurs entre 0° et 180°
        theta1_current = 90 * np.sin(np.radians(frame * 0.5)) + 90
        
        #θ2 varie sinusoïdalement avec une amplitude de 90° et une fréquence de 1.0
        #La formule : 45 * sin(1.0*frame) + 45 donne des valeurs entre 0° et 90°
        theta2_current = 45 * np.sin(np.radians(frame * 1.0)) + 45
        
        #Calcul de l'angle total
        theta_total_current = theta1_current + theta2_current
        
        #------------------------------------------------------------------------
        #2.Calcul des vitesses articulaires(derivees des angles)
        #------------------------------------------------------------------------
        #Dérivée de A*sin(ωt) + C : A*ω*cos(ωt)
        dtheta1 = 90 * 0.5 * np.cos(np.radians(frame * 0.5)) * (np.pi/180)
        dtheta2 = 45 * 1.0 * np.cos(np.radians(frame * 1.0)) * (np.pi/180)
        
        #------------------------------------------------------------------------
        #3.Calculs de cinematique directe 
        #------------------------------------------------------------------------
        x1_curr, y1_curr, x2_curr, y2_curr = cinematique_directe_2dof(
            theta1_current, theta2_current, L1, L2)
        
        #------------------------------------------------------------------------
        #4.Calculs de cinematique differentielle(Jacobien)
        #------------------------------------------------------------------------
        J_curr = calculer_jacobien_2dof(theta1_current, theta2_current, L1, L2)
        det_J_curr = np.linalg.det(J_curr)
        
        #------------------------------------------------------------------------
        #5.Detection des singiularites
        #------------------------------------------------------------------------
        is_singular_curr, _ = detecter_singularites_2dof(theta1_current, theta2_current, L1, L2)
        
        #------------------------------------------------------------------------
        #6.Calcul de la vitessse de l'effecteur
        #------------------------------------------------------------------------
        vx, vy = calculer_vitesse_effecteur_2dof(theta1_current, theta2_current,
                                            dtheta1*180/np.pi, dtheta2*180/np.pi, L1, L2)
        vitesse_norme = np.sqrt(vx**2 + vy**2)
        
        #------------------------------------------------------------------------
        #7.Calcul de la distance depuis l'origine
        #------------------------------------------------------------------------
        distance_curr = np.sqrt(x2_curr**2 + y2_curr**2)
        
        #------------------------------------------------------------------------
        #8.Mise a jour du graphique du bras
        #------------------------------------------------------------------------
        line_anim.set_data([0, x1_curr, x2_curr], [0, y1_curr, y2_curr])
        
        #------------------------------------------------------------------------
        #9.Mise a jour de la trajectoire
        #------------------------------------------------------------------------
        x_history_anim.append(x2_curr)
        y_history_anim.append(y2_curr)
        #Limite la longueur de l'historique pour des raisons de performance
        if len(x_history_anim) > 100:
            x_history_anim.pop(0)
            y_history_anim.pop(0)
        trajectory_anim.set_data(x_history_anim, y_history_anim)
        effecteur_dot_anim.set_data([x2_curr], [y2_curr])
        
        #------------------------------------------------------------------------
        #10.Mise a jour de graphique des angles
        #------------------------------------------------------------------------
        frame_history_anim.append(frame)
        theta1_history_anim.append(theta1_current)
        theta2_history_anim.append(theta2_current)
        theta_total_history_anim.append(theta_total_current)
        #Limite la longueur de l'historique
        if len(frame_history_anim) > 200:
            frame_history_anim.pop(0)
            theta1_history_anim.pop(0)
            theta2_history_anim.pop(0)
            theta_total_history_anim.pop(0)
        
        angle1_line_anim.set_data(frame_history_anim, theta1_history_anim)
        angle2_line_anim.set_data(frame_history_anim, theta2_history_anim)
        angle_total_line_anim.set_data(frame_history_anim, theta_total_history_anim)
        
        #------------------------------------------------------------------------
        #11.Mise a jour des informations textuelles
        #------------------------------------------------------------------------
        info_text = f"""
        Frame: {frame:3.0f}

        Angles:
        θ1 = {theta1_current:6.1f}°
        θ2 = {theta2_current:6.1f}°
        θ1+θ2 = {theta_total_current:6.1f}°

        Positions:
        Base: (0.000, 0.000) cm
        Coude: ({x1_curr:6.2f}, {y1_curr:6.2f}) cm
        Effecteur: ({x2_curr:6.2f}, {y2_curr:6.2f}) cm

        Jacobien(2×2):
        {J_curr[0,0]:6.2f} {J_curr[0,1]:6.2f}
        {J_curr[1,0]:6.2f} {J_curr[1,1]:6.2f}

        Analyse:
        det(J) = {det_J_curr:6.3f}
        Distance = {distance_curr:6.2f} cm
        vx = {vx:6.2f} cm/s
        vy = {vy:6.2f} cm/s
        |v| = {vitesse_norme:6.2f} cm/s

        {'Singulier (sin(θ2)≈0)' if is_singular_curr else 'Normal'}
        """
        info_text_obj.set_text(info_text)
            
            #------------------------------------------------------------------------
            #12.Mise a jour de titre
            #------------------------------------------------------------------------
        axes_anim[0].set_title(f"Bras 2DOF - Frame {frame:.0f}", fontsize=12, fontweight='bold')
            
            #------------------------------------------------------------------------
            #13.Retour des objets a mettre a jour
            #------------------------------------------------------------------------
        return (line_anim, trajectory_anim, effecteur_dot_anim, 
                    angle1_line_anim, angle2_line_anim, angle_total_line_anim, info_text_obj)

        #----------------------------------------------------------------------------
        #Création de l'objet animation
        #----------------------------------------------------------------------------
        ani_advanced = FuncAnimation(
            fig=fig_anim,           #Figure à animer
            func=update_animation,  #Fonction de mise à jour
            frames=np.arange(0, 720, 1.5),  #Séquence de frames : de 0 à 720 par pas de 1.5
            interval=30,            #Intervalle entre les frames en ms (30 ms ≈ 33 fps)
            blit=True,              #Optimisation : ne redessine que ce qui a changé
            repeat=True             #L'animation se répète en boucle
        )

        #----------------------------------------------------------------------------
        #Affichage de l'animation dans Jupyter Notebook
        #----------------------------------------------------------------------------
        print("\nLancement de l'animation avec calculs en temps réel...")
        print("-Cinématique directe (positions)")
        print("-Matrice Jacobienne 2×2")
        print("-Calcul du déterminant")
        print("-Détection de singularités (sin(θ2) ≈ 0)")
        print("-Vitesse de l'effecteur")
        print("-Analyse de mobilité\n")

        #Conversion de l'animation en HTML/JavaScript pour l'affichage dans Jupyter
        display(HTML(ani_advanced.to_jshtml()))

        ani = FuncAnimation(fig, update_animation, frames=np.arange(0,720,1.5), interval=30, blit=True, repeat=True)
        display(HTML(ani.to_jshtml()))
