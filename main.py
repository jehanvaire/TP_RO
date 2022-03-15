from ville import Ville
from utilitaires import *
#from cyberbrain import trace
from tkinter import *
from affichage import *
import time




def plus_proche_voisin(listeV, ville):
    t= []
    t.append(ville)
    
    while len(listeV) > 1:
        _, suivant = plus_proche(listeV, ville)
        t.append(suivant)
        ville = suivant

    return t


def plus_proche_voisin_ameliore(listeVilles):
    listeDistances = []

    for v in listeVilles:
        listeV = listeVilles.copy()
        tournee = plus_proche_voisin(listeV, v)
        listeDistances.append([cout(tournee), tournee])
    
    tournee_min = listeDistances[listeDistances.index(min(listeDistances))][1]

    return tournee_min


def insertion_proche(listeV):

    # on cherche les deux villes les plus éloignées l'une de l'autre
    listeVillesIP = get_villes_plus_eloignees(listeV)
    
    # et on les supprime de la liste de villes
    if(listeVillesIP[0] in listeV and listeVillesIP[1] in listeV):
        listeV.remove(listeVillesIP[0])
        listeV.remove(listeVillesIP[1])
    
    # chaque itération permet de trouver la ville qui étend le moins la tournée
    for i in range(0, len(listeV)):
        distance_min = 9999999999
        index_min = -1
        ville = None
        # on va parcourir la liste de villes pour trouver la ville qui étend le moins la tournée
        for v in listeV:

            # on va chercher l'index auquel la ville ajoutera le moins de distance
            for i in range(0, len(listeVillesIP)):
                # on vérifie si la ville peut prendre la dernière place de la tournée
                if(i == len(listeVillesIP)-1):
                    distance_ajoutee = calculDistance(listeVillesIP[i], v) + calculDistance(v, listeVillesIP[0]) - calculDistance(listeVillesIP[i], listeVillesIP[0])
                # sinon, pour tous les autres éléments de la liste, on calcule la distance ajoutée
                else:
                    distance_ajoutee = calculDistance(listeVillesIP[i], v) + calculDistance(v, listeVillesIP[i+1]) - calculDistance(listeVillesIP[i], listeVillesIP[i+1])
                
                # si la nouvelle distance est mieux, alors on la prends.
                if(distance_ajoutee < distance_min):
                    distance_min = distance_ajoutee
                    index_min = i
                    ville = v
        
        # une fois que la ville et l'index minimum sont trouvés, on insère dans la nouvelle tournée
        listeVillesIP.insert(index_min+1, ville)
        # on enlève la ville de a liste de villes pour éviter qu'elle apparaisse plusieurs fois
        listeV.remove(ville)

    return listeVillesIP



def insertion_loin(listeV):
    # on cherche les deux villes les plus éloignées l'une de l'autre
    listeVillesIL = get_villes_plus_eloignees(listeV)
    
    # et on les supprime de la liste de villes
    if(listeVillesIL[0] in listeV and listeVillesIL[1] in listeV):
        listeV.remove(listeVillesIL[0])
        listeV.remove(listeVillesIL[1])
        
    for v in listeVillesIL:
        print(v.getNum(), end=' ')
        
    for i in range(0, 2):
        distance_max = -1
        index_min = -1
        distance_precedente = 9999999999999
        ville = None

        for v in listeV:

            for i in range(0, len(listeVillesIL)):

                if(i == len(listeVillesIL)-1):
                    distance_ajoutee = calculDistance(listeVillesIL[i], v) + calculDistance(v, listeVillesIL[0]) - calculDistance(listeVillesIL[i], listeVillesIL[0])
                else:
                    distance_ajoutee = calculDistance(listeVillesIL[i], v) + calculDistance(v, listeVillesIL[i+1]) - calculDistance(listeVillesIL[i], listeVillesIL[i+1])
                
                if(distance_ajoutee > distance_max and distance_ajoutee < distance_precedente):
                    if(i == len(listeVillesIL)-1 and i > 0):
                        distance_ajoutee = calculDistance(listeVillesIL[i], ville) + calculDistance(ville, listeVillesIL[0]) - calculDistance(listeVillesIL[i], listeVillesIL[0])
                    elif(i > 0):
                        distance_precedente = calculDistance(listeVillesIL[i], ville) + calculDistance(ville, listeVillesIL[i+1]) - calculDistance(listeVillesIL[i], listeVillesIL[i+1])
                    distance_max = distance_ajoutee
                    index_min = i
                    ville = v
        listeVillesIL.insert(index_min+1, ville)
        listeV.remove(ville)

    return listeVillesIL




def affiche_tournee(listeVAAFF, listeComplete):
    canv = Canvas(root, width=largeur, height=hauteur)

    canv.delete("all")
    canv.create_image(0, 0, anchor=NW, image=photo)

    canv.pack(expand=YES, fill="both")
    for i in range(0, len(listeVAAFF)-1):
        x, y = fromLatLong2pixels(listeVAAFF[i], listeComplete, largeur, hauteur)
        xSuiv, ySuiv = fromLatLong2pixels(listeVAAFF[i+1], listeComplete, largeur, hauteur)
        y = hauteur - y
        ySuiv = hauteur - ySuiv

        canv.create_line(x, y, xSuiv, ySuiv)
        canv.create_text(x, y, text=str(listeVAAFF[i].getNum()))
        canv.pack()

        if (i == len(listeVAAFF)-1):
            xSuiv, ySuiv = fromLatLong2pixels(listeVAAFF[0], listeComplete, largeur, hauteur)
            ySuiv = hauteur - ySuiv
            canv.create_line(x, y, xSuiv, ySuiv)





if __name__ == "__main__":

    #CHARGEMENT DES DONNEES
    #============================================================#
    f = open("instances/top80.txt", "r")
    lines = f.readlines()
    listeVilles = []

    tourneeVilles = []

    hauteur = 754
    largeur = 686



    for x in lines:
        ville = x.split(" ")
        v = Ville(ville[0], ville[1], ville[2], ville[3])
        listeVilles.append(v)

    listeVillesCopie = listeVilles.copy()


    root = Tk(className='TP recherche opérationnelle')
    root.geometry("686x754")

    photo = PhotoImage(file="carte.png")
    
    #============================================================#


    listeVillesIP = insertion_proche(listeVillesCopie)

    for i in range(0, len(listeVillesIP)-1):
        petiteListe = listeVillesIP[0:i]
        print(len(petiteListe))

        affiche_tournee(petiteListe, listeVillesIP)
        time.sleep(0.1)

        root.mainloop()


    
    # listeVillesCopie = listeVilles.copy()
    # distanceTotaleOrdre = cout(listeVillesCopie)
    # print(f"Distance totale parcourue ordre croissant: {distanceTotaleOrdre} km")
    # print(f"Chemin utilise dans l'ordre : {afficheTour(listeVilles)}\n\n")

    # print(f"Ville la plus proche de {listeVilles[0].getNom()} : {plus_proche(listeVilles, listeVilles[0])[1].getNom()}")

    # listeVillesCopie = listeVilles.copy()


    # listeVillesCopie = tourAleatoire(listeVillesCopie)
    # distanceTotale = cout(listeVillesCopie)
    # print(f"Distance totale parcourue aleatoire: {distanceTotale} km")
    # print(f"Chemin utilise aleatoire : {afficheTour(listeVillesCopie)}\n\n")

    # listeVillesCopie = listeVilles.copy()

    # print("Ville 1 " + listeVillesCopie[0].getNom())
    # tournee_glouton = plus_proche_voisin(listeVillesCopie, listeVilles[0])
    # print(f"Chemin utilise dans glouton : {afficheTour(tournee_glouton)}")
    # print(f"Distance totale parcourue glouton : {cout(tournee_glouton)} km\n\n")

    #On rempli listeVillesCopie vu que celle-ci se vide dans la méthode plus_proche_voisin
    # listeVillesCopie = listeVilles.copy()

    # tournee_glouton_ameliore = plus_proche_voisin_ameliore(listeVillesCopie)
    # print(f"Chemin utilise dans glouton ameliore : {afficheTour(tournee_glouton_ameliore)}")
    # print(f"Distance totale parcourue glouton ameliore: {cout(tournee_glouton_ameliore)} km\n\n")

    
    # listeVillesCopie = listeVilles.copy()
    


    # listeVillesIP1 = insertion_proche(listeVillesCopie)
    # print(f"Chemin utilise dans insertion proche : {afficheTour(listeVillesIP1)}")
    # print(f"Distance totale parcourue insertion proche : {cout(listeVillesIP1)} km\n\n")

    # listeVillesCopie = listeVilles.copy()


    # listeVillesIL = insertion_loin(listeVillesCopie)
    # print(f"Chemin utilise dans insertion loin : {afficheTour(listeVillesIL)}")
    # print(f"Distance totale parcourue insertion loin : {cout(listeVillesIL)} km\n\n")