# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 9:28:12 2023

@author: Malo
"""
#------------------------------------------------------------------------------
'''
Projet de programmation M1 Physique Fondamentales & Applications
Parcours Photonique

Modélisation de la réflexion d'un paquet d'ondes sur une marche de potentiel 
de hauteur variable. Résolution par décomposition en ondes stationnaires.
'''
#------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider,RadioButtons,Button
from matplotlib.animation import FuncAnimation
from paquet_onde import V0,k,Ak,Ek,phi_libre,evolution,phi_step,phi_i,phi_r,phi_t
#------------------------------------------------------------------------------

# initialisation des graphes
fig, (ax1, ax2) = plt.subplots(2,1,gridspec_kw={'height_ratios': [2, 1]},\
                               figsize=(13,8))
plt.subplots_adjust(bottom=0.3, top=0.95, left=0.02, right=0.98)
ax1.set(xlim=(-2, 2), ylim=(-17, 17))
ax1.set_title("Réflexion d'un paquet d'ondes sur une marche de potentiel variable")
line1,= ax1.plot([], [], color='mediumblue')
line2,= ax1.plot([], [], color='cornflowerblue')
line3,= ax1.plot([], [], color='chocolate')
font = {'size': 11}
plt.text(0.5,-0.85,"Choisir une animation avec ou sans potentiel grâce aux boutons.",\
             fontdict=font)
plt.text(0.5,-1,"Utiliser le slider pour faire varier la hauteur de la marche $V_0$ (en mode 'Marche').",\
         fontdict=font)
ax1.grid()
ax2.set(xlim=(0,7500))
extraticks=[2500,5000,7500]
ax2.set_xticks([0,10000])
ax2.set_xticks(list(ax2.get_xticks()) + extraticks)
ax2.set_xticklabels(['$0$','$2E_0$','$0.5E_0$','$E_0$','$1.5E_0$'])
axis_param = ax1.xaxis.get_major_ticks() + ax1.yaxis.get_major_ticks() +\
    ax2.yaxis.get_major_ticks()
plotpot = ax2.bar(Ek,Ak,color="mediumblue",width=4,snap=False)
plotvarpot = ax2.axvline(x=V0,color="chocolate")

def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    return line1,line2,line3

for tick in axis_param:
    tick.tick1line.set_visible(False)
    tick.tick2line.set_visible(False)
    tick.label1.set_visible(False)
    tick.label2.set_visible(False)

# Espace des x :
xmin = -2
xmax = 2
N = 1500
x = np.linspace(xmin,xmax,N)
x1 = np.linspace(xmin,0,int(N/2))
x2 = np.linspace(0,xmax,int(N/2))

# Paramètres d'échelles pour l'affichage
scale = 1e-3
T = 2e-4
t0 = 0.029

# Affichage de la propagation sans potentiel par défaut
potentiel="Marche"

# Initialisation des sliders et boutons
ax_radio = plt.axes([0.83, 0.11, 0.14, 0.14], facecolor='0.9')
radio = RadioButtons(ax_radio, ("Paquet d'ondes","Marche"),\
                     activecolor='cornflowerblue',active=1)

ax_newstep = plt.axes([0.05, 0.22, 0.77, 0.03])
s_newstep = Slider(ax_newstep, '$V_0$', 0.0, 7.5, valinit=scale*V0,\
                   color='cornflowerblue', initcolor='none', dragging=True)
s_newstep.valtext.set_visible(False)

ax_reset = plt.axes([0.68, 0.11, 0.14, 0.04])
button = Button(ax_reset, 'Reset',hovercolor='0.975')

#------------------------------------------------------------------------------

# Création de la fonction marche de potentiel
def V(x,V0):
    return V0*(np.sign(x)+1)
plotstep, = ax1.plot(x, V(x,V0*scale),'--',color='k')

# Boutons pour changer le type de potentiel + update plot
def potentiel_plot(label):
    global potentiel
    potentiel = label
    if potentiel == "Paquet d'ondes":
        ax1.set_title("Propagation d'un paquet d'ondes")
        plotstep.set_data([],[])
    if potentiel == "Marche":
        ax1.set_title("Réflexion d'un paquet d'ondes sur une marche de potentiel variable")
        plotstep.set_data(x, V(x,V0*scale))
        fig.canvas.draw()
    return plotstep

# Fonction d'animation avec i le nombre de frames
def animate(i):
    if potentiel == "Paquet d'ondes":
        y = evolution(phi_libre,Ak,Ek,i*T-t0)
        line1.set_data(x,y)
        line2.set_data([],[])
        line3.set_data([],[])
    if potentiel == "Marche":
        y1 = evolution(phi_i,Ak,Ek,i*T-t0) 
        y2 = evolution(phi_r,Ak,Ek,i*T-t0) 
        y3 = evolution(phi_t,Ak,Ek,i*T-t0) 
        line1.set_data(x1,y1)
        line2.set_data(x1,y2)
        line3.set_data(x2,y3)
    return line1,line2,line3

# Update la valeur et calculs des nouveaux psi
def update_plot_step(val):
    global phi_i,phi_r,phi_t,anim
    if potentiel == "Marche":
        plotstep.set_ydata(val*(np.sign(x) + 1))
        phi_i,phi_r,phi_t = phi_step(k,x,val/scale)
        plotvarpot.set_xdata(val/scale)
    if potentiel == "Paquet d'ondes":
        plotvarpot.set_xdata(val/scale)

# Bouton reset du slider
def reset(event):   
    s_newstep.reset()

radio.on_clicked(potentiel_plot)
s_newstep.on_changed(update_plot_step)
button.on_clicked(reset)
anim = FuncAnimation(fig,animate,init_func=init,frames=300,interval=10,\
                     repeat=True,cache_frame_data=False)
plt.show()