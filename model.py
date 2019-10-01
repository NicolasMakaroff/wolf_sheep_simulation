from tkinter import *
from math import *
from random import randrange
import random
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import randrange
haut =50 #hauteur du tableau
larg =50 #largeur du tableau
cote =10  #dimension d'une case
loup=1
mouton=2
mort=3
compteur=0 #variable locale qui va servir à compter le nombre de boucles réalisées pendant l'exécution du programme
nmout=[]
nloup=[]#ces deux listes vont servir à tracer le graphe du nombre de loups et de moutons en fonction du temps



cell = [[3 for k in range(haut)] for i in range (larg)]
etat = [[[3,10,0] for i in range(haut)] for j in range(larg)]
temp = [[[3,10,0] for i in range(haut)] for j in range(larg)]


#on renvoie une liste de listes à deux éléments indiquant les coordonnées des cases du voisinage de la case de coordonnées (x,y)
def liste_pratique(x,y):
    if x==0:
        if y==0:
            return [[x,y+1],[x+1,y],[x+1,y+1]]
        if y==larg-1:
            return [[x,y-1],[x+1,y],[x+1,y-1]]
        else:
            return [[x,y-1],[x+1,y-1],[x+1,y],[x+1,y+1],[x,y+1]]
    if x==haut-1:
        if y==0:
            return [[x-1,y],[x,y+1],[x-1,y+1]]
        if y==larg-1:
            return [[x,y-1],[x-1,y-1],[x-1,y]]
        else:
            return [[x,y-1],[x-1,y-1],[x-1,y],[x-1,y+1],[x,y+1]]
    if y==0:
        return [[x-1,y],[x-1,y+1],[x,y+1],[x+1,y+1],[x+1,y]]
    if y==larg-1:
        return [[x-1,y],[x-1,y-1],[x,y-1],[x+1,y-1],[x+1,y]]
    return [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]]


# calculer et dessiner le prochain tableau
def tableau():
    calculer()
    dessiner()
    fenetre.after(100, tableau)
    
#on place les entités dans la matrice       
def init():
    for y in range(haut):
        for x in range(larg):
            etat[x][y] = [3,10,0]
            temp[x][y] = [3,10,0]
            cell[x][y] = canvas.create_rectangle((x*cote, y*cote,
            (x+1)*cote, (y+1)*cote), outline="gray", fill="white")
    # placer au hasard environ 1% de loups
    for i in range(larg*haut//20):
        etat[randrange(larg)][randrange(haut)]=[loup,10,0]
    #placer au hasard environ 1% de moutons
    for i in range(larg*haut//2):
        etat[randrange(larg)][randrange(haut)]=[mouton,10,0]
            
        
# renvoie le nombre de moutons du voisinage de la case (x,y)
def nb_moutons_adj(x,y):
    return len(liste_moutons(x,y))


#on renvoie une liste de listes à deux éléments indiquant les coordonnées des éventuels moutons du voisinage de la case (x,y)
def liste_moutons(x,y):
    L=liste_pratique(x,y)
    mout=[]
    for i in range(len(L)):
        if etat[L[i][0]][L[i][1]][0]==mouton:
            mout.append(L[i])
    return mout
    
#le loup mange un mouton choisi au hasard parmi ses voisins (avec une chance de 95%)        
def manger_mouton(x,y):
    n=randrange(100)
    if n>=5:
        M = liste_moutons(x,y)
        if len(M)!=0:
            N = random.choice(M)#on choisit au hasard un mouton du voisinage et le loup le mange
            temp[N[0]][N[1]][0] = loup
            temp[N[0]][N[1]][1] = etat[x][y][1]+15
            temp[N[0]][N[1]][2] = etat[x][y][2]+1
            temp[x][y] = [mort,10,0]
        else:
            #si aucun mouton n'est dans les parages, le loup se déplace
            deplacement_aleatoire_loup(x,y)
            

#le loup se déplace aléatoirement sur une case non occupée de son voisinage 
def deplacement_aleatoire_loup(x,y):
    L=liste_pratique(x,y)
    l=[]
    for i in range(len(L)):
        #on regarde les cases non occupées du voisinage de la case (x,y)
        if etat[L[i][0]][L[i][1]][0]!=loup and etat[L[i][0]][L[i][1]][0]!=mouton:
            l.append(L[i])
    if len(l) !=0:
        N=random.choice(l)
        temp[N[0]][N[1]][0] = loup
        temp[N[0]][N[1]][1]=  etat[x][y][1]-2
        temp[N[0]][N[1]][2]=  etat[x][y][2]+1
        temp[x][y] = [mort,10,0]
        #le loup s'est déplacé sur une case disponible de son voisinage, choisie aléatoirement
    else:
        #si aucune case n'est disponible, le loup reste sur place
        temp[x][y][1]=etat[x][y][1]-2
        temp[x][y][2]=etat[x][y][2]+1
    
    
#le mouton se déplace aléatoirement sur une case non occupée de son voisinage (fonctionnement similaire à celui de la fonction de déplacement des loups)       
def deplacement_aleatoire_mouton(x,y):
    L=liste_pratique(x,y)
    m=[]
    for i in range(len(L)):
        if etat[L[i][0]][L[i][1]][0]!=loup and etat[L[i][0]][L[i][1]][0]!=mouton:
            m.append(L[i])
    if len(m) !=0:
        N=random.choice(m)
        temp[N[0]][N[1]] = [mouton,10,etat[x][y][2]+1]
        temp[x][y] = [mort,10,0]
    else:
        temp[x][y][2]=etat[x][y][2]+1
 
#un mouton naît sur une case non occupée du voisinage d'un mouton       
def spawn_mouton(x,y):
    n=randrange(10)
    if n>=9:#pour éviter que les moutons ne se reproduisent trop rapidement, on fait en sorte que la naissance d'un agneau ne se fasse pas de manière systématique
        L=liste_pratique(x,y)
        m=[]
        for i in range(len(L)):
            #on regarde si les cases alentours ne sont pas occupées
            if etat[L[i][0]][L[i][1]][0]!=mouton and etat[L[i][0]][L[i][1]][0]!=loup:
                m.append(L[i])
        if len(m)!=0:
            #on fait apparaître un mouton sur une des cases non occupées du voisinage, si toutes les cases sont occupées, rien ne se passe
            N=random.choice(m)
            temp[N[0]][N[1]]=[mouton,10,0]
            

#un loup naît sur une case non occupée du voisinage d'un loup(fonctionnement similaire à celui de la fonction faisant naître des moutons)    
def spawn_loup(x,y):
    L=liste_pratique(x,y)
    l=[]
    for i in range(len(L)):
        if etat[L[i][0]][L[i][1]][0]!=mouton and etat[L[i][0]][L[i][1]][0]!=loup:
            l.append(L[i])
    if len(l)!=0:
        N=random.choice(l)
        temp[N[0]][N[1]]=[loup,7,0]
        temp[x][y][1]=etat[x][y][1]-10
        temp[x][y][2]=etat[x][y][2]+1
    else:
        deplacement_aleatoire_loup(x,y)

def calculer():
    global etat,nmout,nloup
    nbloup,nbmout=0,0 #variables locales qui vont servir à compter le nombre de moutons et de loups à chaque boucle
    for x in range(haut):
        for y in range(larg):
            #gestion des loups
            if etat[x][y][0] == loup:
                nbloup=nbloup+1
                #règle 1 = un loup trop vieux ou sans energie meurt
                if etat[x][y][1]<=0 or etat[x][y][2]>=30:
                    temp[x][y][0]=[mort,10,0]
                #règle 2 = un loup mange un mouton
                elif nb_moutons_adj(x,y)!=0:
                    manger_mouton(x,y)
                #règle 3 = reproduction
                if etat[x][y][2]>=15 and etat[x][y][1]>=10:
                    spawn_loup(x,y)
                
                #règle 4 = déplacement du loup 
                else:
                    deplacement_aleatoire_loup(x,y)
            #gestion des moutons
            if etat[x][y][0] == mouton:
                nbmout=nbmout+1
                #règle 1 = un mouton trop vieux meurt
                if etat[x][y][2] >=30:
                    temp[x][y] = [mort,10,0]
                #règle 2 = reproduction
                if etat[x][y][2] >= 15:
                    n=randrange(10)
                    if n>5:
                        spawn_mouton(x,y)
                    else:
                        deplacement_aleatoire_mouton(x,y)
    nmout.append(nbmout)
    nloup.append(nbloup)
    etat=deepcopy(temp)
                    
# dessiner et calculer la prochaine grille        
def dessiner():
    global compteur
    for y in range(haut):
        for x in range(larg):
            if etat[x][y][0]==1:
                #on dessine les loups
                coul = "gray"
            elif etat[x][y][0]==2:
                #on dessine les moutons
                coul = "white"
            else:
                #on dessine l'herbe(les cases mortes, non occupées)
                coul = "green"
            canvas.itemconfig(cell[x][y], fill=coul)    
    Bouton.configure(text=str(compteur))
    compteur+=1

#On lance le programme
fenetre = Tk()
fenetre.title("Loups vs moutons")
canvas = Canvas(fenetre, width=cote*larg+10, height=cote*haut+10,highlightthickness=0)
canvas.pack()
Bouton= Label(fenetre,  text='blabla')
Bouton.pack(side=RIGHT)
init()
dessiner()
tableau()  
fenetre.mainloop()

#On trace les graphes du nombre de loups et de moutons en fonction du temps
plt.plot([t for t in range(compteur-1)],nmout)
plt.plot([t for t in range(compteur-1)],nloup)
plt.show()
