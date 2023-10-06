# -*- coding: utf-8 -*-
"""
Created on Fri Feb 03 9:28:12 2023

@author: Ronan
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
#------------------------------------------------------------------------------

# Espace des k :
k0 = 100 # nombre d'onde central
E0 = 0.5*k0**2
sigma_k = 5 # largeur gaussienne, écart-type en impulsion
delta_k = 1

# Espace des x :
xmin = -2
xmax = 2
N = 1500 # nombre de points
x = np.linspace(xmin,xmax,N)
x1 = np.linspace(xmin,0,int(N/2))
x2 = np.linspace(0,xmax,int(N/2))

# Potentiel
V0 = 1.3*E0

def spectre_gaussien(k0,sigma_k,delta_k):
    """
    Parameters
    ----------
    k0 : INT
        Nombre d'onde central du spectre gaussien.
    sigma_k : INT
        Ecart-type en impulsion, largeur de la gaussienne.
    delta_k : écart de nombre d'onde entre deux raies du spectre.

    Returns
    -------
    k : ARRAY OF FLOAT
        Tableau des nombres d'onde des raies du spectre gaussien.
    Ak : ARRAY OF FLOAT
        Tableau des amplitudes des raies du spectre gaussien .
    Ek : ARRAY OF FLOAT
        Tableau des énergies des raies du spectre gaussien.
    """
    kmin = k0-int(4*sigma_k) # nombre d'onde minimal
    kmax = k0+int(4*sigma_k) # nombre d'onde maximal
    k = np.arange(kmin,kmax+delta_k,delta_k)
    Ak = np.zeros(k.size) # tableau vide pour les amplitudes
    Ek = np.zeros(k.size) # tableau vide pour les énergies
    for i in range(len(k)):
        Ak[i] = np.exp(-(k[i]-k0)**2/(2*sigma_k**2))
        Ek[i] = 0.5*k[i]**2
    
    return k,Ak,Ek

k,Ak,Ek = spectre_gaussien(k0,sigma_k,delta_k)

def phi_libre(k,x): 
    """
    Parameters
    ----------
    k : ARRAY OF FLOAT
        Tableau des nombres d'ondes des raies du spectre gaussien.
    x : ARRAY OF FLOAT
        Points de calcul des états stationnaires du paquet d'onde libre.

    Returns
    -------
    phi_libre : ARRAY OF ARRAY OF COMPLEXS
            Tableau des valeurs des k états stationnaires en chaque point x.
    """
    phi_libre = np.zeros((x.size,k.size),dtype=complex)
    
    for i in range(len(x)):
        for j in range(len(k)):
            phi_libre[i][j] = np.exp(1j*k[j]*x[i])
        
    return phi_libre

phi_libre=phi_libre(k,x)

def phi_step(k,x,V0):
    """
    Parameters
    ----------
    k : ARRAY OF FLOAT
        Tableau des nombres d'ondes des raies du spectre gaussien.
    x : ARRAY OF FLOAT
        Points de calcul des états stationnaires du paquet d'onde libre.
    V0 : FlOAT
        Valeur de la marche de potentiel

    Returns
    -------
    phi_step : ARRAY OF ARRAY OF COMPLEXS
            Tableau des valeurs des k états stationnaires en chaque point x.
    """
    
    x1 = np.linspace(x[0],0,int(len(x)/2))
    x2 = np.linspace(0,x[-1],int(len(x)/2))
    
    phi_i = np.zeros((x1.size,k.size),dtype=complex)
    phi_r = np.zeros((x1.size,k.size),dtype=complex)
    phi_t = np.zeros((x2.size,k.size),dtype=complex)
    
    for i in range(len(x1)):
        for j in range(len(k)):
            k1 = k[j]
            phi_i[i][j] = np.exp(1j*k1*x1[i])
            if Ek[j]>V0:
                k2 = np.sqrt(2*(Ek[j]-V0))
                r = (k1-k2)/(k1+k2)
                t = 2*k1/(k1+k2)
                phi_r[i][j] = r*np.exp(-1j*k1*x1[i])
                phi_t[i][j] = t*np.exp(1j*k2*x2[i])
                
            else:
                k2 = np.sqrt(2*(V0-Ek[j]))
                r = (k1-1j*k2)/(k1+1j*k2)
                t = 2*k1/(k1+1j*k2)
                phi_r[i][j] = r*np.exp(-1j*k1*x1[i])
                phi_t[i][j] = t*np.exp(-k2*x2[i])
                
    
    return phi_i,phi_r,phi_t
                
phi_i,phi_r,phi_t = phi_step(k,x,V0)
  
def evolution(phi_x,Ak,Ek,t):
    """
    Parameters
    ----------
    phi_x : ARRAY OF ARRAY OF COMPLEXS
        Tableau donnant pour chaque x les valeurs des k états stationnaires.
    Ak : ARRAY OF FLOAT
        Tableau des amplitudes des raies du spectre gaussien .
    Ek : ARRAY OF FLOAT
        Tableau des énergies des raies du spectre gaussien.
    t : FLOAT
        Instant de calcul de la fonction d'onde.

    Returns
    -------
    psi_t : ARRAY OF COMPLEX
        Valeur de la fonction d'onde totale en chaque point x à l'instant t.
    """
    expEk = np.zeros(k.size,dtype=complex)
    for j in range(len(Ek)):
        expEk[j] = np.exp(-1j*Ek[j]*t)
    
    psi_t = np.einsum('j,ij,j->i',Ak,phi_x,expEk)
    
    return psi_t

