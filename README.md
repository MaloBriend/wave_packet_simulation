# Animation de l’évolution d’un paquet d’onde quantique

## Objectifs
Ce projet informatique a pour but de modéliser la réflexion ou le franchissement d’un paquet d’onde au niveau d’une marche de potentiel. Le résultat final rend compte des phénomènes quantiques selon la hauteur de la marche de potentiel. La résolution du paquet d’onde fera intervenir les états stationnaires.

## Principe physique
Le problème physique auquel nous sommes confrontés ici consiste essentiellement à résoudre l'équation de Schrödinger indépendante du temps dans les différentes régions de l'espace caractérisées par la présence ou l'absence d'un potentiel constant (cf. [1]). Cette résolution nous conduit aux expressions des états stationnaires du problème, qui nous servirons de base de décomposition pour notre paquet d'onde.

Considérons ainsi l'exemple d'une particule de masse $m$ associée à la fonction d'onde $\Psi(x,t)$, se déplaçant selon un axe $Ox$ et soumise à une marche de potentiel $V(x)$, comme représenté sur la figure 1 ci-dessous. En s'intéressant uniquement aux états stationnaires de cette particule, sa fonction d'onde se réécrit 
$\Psi(x,t) = \phi(x)e^{-iEt/\hbar}$, la partie spatiale $\phi(x)$ vérifiant l'équation de Schrödinger indépendante du temps :

$$\begin{align}
H\phi(x) = E\phi(x)
\end{align}$$

où $E$ est l'énergie de la particule.

<img src="https://github.com/MaloBriend/wave_packet_simulation/blob/main/marche_potentiel.png" width="400" />
Fig 1. Marche de potentiel. Le saut de potentiel se fait en x=0.

- Au niveau de la région 1, la particule n'est soumise à aucun potentiel et se comporte comme une particule libre.

$$\begin{align}
\frac{d^2\phi_1(x)}{dx^2} + \frac{2mE}{\hbar^2}\phi_1(x) = 0
\end{align}$$

La solution générale de cette équation est la somme d'une onde plane progressive et d'une onde plane régressive :

$$\begin{align}
\phi_1(x) = A_1e^{ik_1x} + rA_1e^{-ik_1x}~avec~k_1 = \sqrt{\frac{2mE}{\hbar^2}}
\end{align}$$

- Au niveau de la région 2, la particule est soumise à un potentiel constant $V_0$.

$$\begin{align}
\frac{d^2\phi_2(x)}{dx^2} + \frac{2m(E-V_0)}{\hbar^2}\phi_2(x) = 0
\end{align}$$

Si $E > V_0$ la solution de cette équation est onde une plane :

$$\begin{align}
\phi_2(x) = t~A_1e^{ik_2x}~avec~k_2 = \sqrt{\frac{2m(E-V_0)}{\hbar^2}}
\end{align}$$

et les coefficients de réflexion $r$ et de transmission $t$ s'écrivent :

$$\begin{align}
r=\frac{k_1-k_2}{k_1+k_2}~~;~~t=\frac{2k_1}{k_1+k_2}
\end{align}$$

Si $E < V_0$ la solution de cette équation est une onde évanescente :

$$\begin{align}
\phi_2(x) = t~A_1e^{-k_2x}~avec~k_2 = \sqrt{\frac{2m(V_0-E)}{\hbar^2}}
\end{align}$$

et les coefficients de réflexion $r$ et de transmission $t$ s'écrivent :

$$\begin{align}
r=\frac{k_1-ik_2}{k_1+ik_2}~~;~~t=\frac{2k_1}{k_1+ik_2}
\end{align}$$

*Par la suite, il sera utile de travailler en unité atomique, avec* $\hbar = 1$ et $m = 1$.

La résolution de ce problème nous permet donc de conclure que :
- il existe une probabilité non nulle que la particule soit réfléchie lorsque son énergie est supérieure à celle de la marche de potentiel.
- il existe une probabilité de présence non nulle de la particule dans la région 2 lorsque son énergie est inférieure à celle de la marche de potentiel, ce qui traduit une certaine profondeur de pénétration.

L'objectif de notre projet est ainsi de mettre en évidence visuellement ces deux phénomènes, en associant cependant la particule à une fonction d'onde de type paquet d'onde gaussien:

$$\begin{align}
\Psi(x,t) = \phi(x)e^{-iEt/\hbar} = G(x)e^{ikx}e^{-iEt/\hbar}
\end{align}$$

où $G(x)$ est une enveloppe gaussienne évoluant en $e^{-x^2}$, modulant l'amplitude de la porteuse $e^{ikx}e^{-iEt/\hbar}$. En assimilant un tel paquet d'onde à une superposition d'ondes planes de nombres d'onde k différents, nous pouvons envisager de résoudre le problème de la marche de potentiel en décomposant ce paquet sur les états stationnaires établis plus tôt, et donc de faire appel à la transformation de Fourier pour passer de l'espace des positions [x] à l'espace des nombres d'onde [k], et réciproquement.

<img src="https://github.com/MaloBriend/wave_packet_simulation/blob/main/paquet.png" width="400" />
Fig 2. Paquet d'onde gaussien se propageant vers une marche de potentiel.

## Techniques informatiques

Pour ce projet, nous utiliserons le langage de programmation Python muni principalement des bibliothèques *numpy* et *matplotlib*. Pour animer notre projet et le rendre simple à utiliser, nous tirerons profit de *matplotlib.widgets* pour intégrer des sliders et ainsi contrôler certains paramètres. De plus le module *FuncAnimation* permettra d'animer l'ensemble.

## Mode d'emploi
Pour utiliser correctement notre programme, il faut s'assurer tout d'abord d'entrer la ligne de commande *\%matplotlib qt* pour visualiser correctement l'animation. Ensuite il faut exécuter le fichier *animation* en s'assurant que le fichier *paquet\_onde* existe bien dans le même dossier.

Par défaut, l'animation affiche la propagation d'un paquet d'onde sur une marche de potentiel. La hauteur de la marche peut être modifiée via le curseur $V_0$, l'animation se mettra à jour automatiquement. Un bouton reset permet de revenir à la position initiale. De plus, grâce aux boutons sur la droite, il est possible de choisir soit l'animation d'un paquet d'onde devant une marche de potentiel, soit la propagation simple d'un paquet d'onde.

<img src="https://github.com/MaloBriend/wave_packet_simulation/blob/main/interface.png" width="400" />
Fig 3. Interface de notre programme

---

Acknowledgement : Ronan Piedevache

[1] Mehdi Ayouz et al. Les Fondamentaux de La Mécanique Quantique Sous Python : Rappel de Cours et Exercices d’application Avec Programmes Inclus. HAL CCSD, 1er jan. 2020.
