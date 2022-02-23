from ville import Ville
from utilitaires import *
from cyberbrain import trace
from tkinter import *
from affichage import *




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


    for i in range(0, len(listeV)):

        villeChoisie = listeV[0] #ville choisie au hasard
        index = -1

        # on parcour toute la liste de ville pour trouver la prochaine ville 
        # dont le cout sera le plus faible
        for ville in listeV:
            # on copie la liste de villes pour éviter les problèmes
            # on calcule le cout de cette tournée
            # puis on supprime la ville de la liste de test
            distanceIndexOptimal = 99999999
            distancePrecedente = 99999999



            # on trouve l'index auquel la distance sera la plus petite
            for pos in range(1, len(listeVillesIP)):
                listeVillesIP.insert(pos, ville)
                distanceTournee = cout(listeVillesIP)
                listeVillesIP.remove(ville)

                if(distanceTournee < distanceIndexOptimal):
                    distanceIndexOptimal = distanceTournee
                    index = pos
                

            # on insère la ville au meilleur index possible
            listeVillesIP.insert(index, ville)
            # puis on recalcule le cout de la tournée
            distanceTournee = cout(listeVillesIP)
            # print(f'Distance : {distanceTournee}, ville : {ville}')
            listeVillesIP.remove(ville)


            # si le cout de cette tournée est inférieur au cout de la tournée précédente
            # on considère que cette tournée est (pour le moment) la meilleure
            if(distanceTournee < distancePrecedente):
                if(villeChoisie in listeVillesIP):
                    listeVillesIP.remove(villeChoisie)
                villeChoisie = ville
                distancePrecedente = distanceTournee
                listeVillesIP.insert(index, villeChoisie)

        listeV.remove(ville)

    return listeVillesIP



def insertion_loin(listeV):
    listeVillesIP = get_villes_plus_eloignees(listeV)

    if(listeVillesIP[0] in listeV and listeVillesIP[1] in listeV):
        listeV.remove(listeVillesIP[0])
        listeV.remove(listeVillesIP[1])

    
    for i in range(0, len(listeV)):
        villeChoisie = listeV[0] #ville choisie au hasard
        index = -1

        # on parcour toute la liste de ville pour trouver la prochaine ville 
        # dont le cout sera le plus faible

        for ville in listeV:
            # on copie la liste de villes pour éviter les problèmes
            # on calcule le cout de cette tournée
            # puis on supprime la ville de la liste de test
            distanceIndexOptimal = -1
            distancePrecedente = -1
            
            # on trouve l'index auquel la distance sera la plus petite
            for pos in range(1, len(listeVillesIP)):
                listeVillesIP.insert(pos, ville)
                distanceTournee = cout(listeVillesIP)
                listeVillesIP.remove(ville)

                if(distanceTournee > distanceIndexOptimal):
                    distanceIndexOptimal = distanceTournee
                    index = pos


            # on insère la ville au meilleur index possible
            listeVillesIP.insert(index, ville)
            # puis on recalcule le cout de la tournée
            distanceTournee = cout(listeVillesIP)
            # print(f'Distance : {distanceTournee}, ville : {ville}')
            listeVillesIP.remove(ville)

            # si le cout de cette tournée est inférieur au cout de la tournée précédente
            # on considère que cette tournée est (pour le moment) la meilleure
            if(distanceTournee > distancePrecedente):
                if(villeChoisie in listeVillesIP):
                    listeVillesIP.remove(villeChoisie)
                villeChoisie = ville
                distancePrecedente = distanceTournee
                listeVillesIP.insert(index, villeChoisie)

        listeV.remove(ville)
    return listeVillesIP

def create_circle(x, y, r, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill="#FF0000")






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
    canv = Canvas(root, width=largeur, height=hauteur)
    canv.create_image(0, 0, anchor=NW, image=photo)

    canv.pack(expand=YES, fill="both")
    #============================================================#


    listeVillesIP = insertion_proche(listeVillesCopie)
    for v in listeVillesIP:
        print(str(v))

    listeVillesCopie = listeVilles.copy()

    for pos in range(0, len(listeVillesCopie)):
        x, y = fromLatLong2pixels(listeVillesCopie[pos], listeVillesCopie, largeur, hauteur)
        y = hauteur - y
        create_circle(x, y, 5, canv)
        Label(root, text=listeVillesCopie[pos].getNum(), fg="black").place(x=x, y=y)
        if pos > 0:
            xPrecedent, yPrecedent = fromLatLong2pixels(listeVillesCopie[pos-1], listeVillesCopie, largeur, hauteur)
            canv.create_line(xPrecedent, xPrecedent, x, y)



    root.mainloop()


    # distanceTotaleOrdre = cout(listeVilles)
    # print(f"Distance totale parcourue ordre croissant: {distanceTotaleOrdre} km")
    # print(f"Chemin utilise dans l'ordre : {afficheTour(listeVilles)}\n\n")

    # print(f"Ville la plus proche de {listeVilles[0].getNom()} : {plus_proche(listeVilles, listeVilles[0])[1].getNom()}")


    # tourAleatoire(listeVilles)
    # distanceTotale = cout(listeVilles)
    # print(f"Distance totale parcourue aleatoire: {distanceTotale} km")
    # print(f"Chemin utilise aleatoire : {afficheTour(listeVilles)}\n\n")

    # tournee_glouton = plus_proche_voisin(listeVillesCopie, listeVilles[0])
    # print(f"Chemin utilise dans glouton : {afficheTour(tournee_glouton)}")
    # print(f"Distance totale parcourue glouton : {cout(tournee_glouton)} km\n\n")

    # #On rempli listeVillesCopie vu que celle-ci se vide dans la méthode plus_proche_voisin
    # listeVillesCopie = listeVilles.copy()

    # tournee_glouton_ameliore = plus_proche_voisin_ameliore(listeVillesCopie)
    # print(f"Chemin utilise dans glouton ameliore : {afficheTour(tournee_glouton_ameliore)}")
    # print(f"Distance totale parcourue glouton ameliore: {cout(tournee_glouton_ameliore)} km\n\n")

    
    # listeVillesCopie = listeVilles.copy()


    # listeVillesIP = insertion_proche(listeVillesCopie)
    # print(f"Chemin utilise dans insertion proche : {afficheTour(listeVillesIP)}")
    # print(f"Distance totale parcourue insertion proche : {cout(listeVillesIP)} km\n\n")

    # listeVillesCopie = listeVilles.copy()


    # listeVillesIL = insertion_loin(listeVillesCopie)
    # print(f"Chemin utilise dans insertion loin : {afficheTour(listeVillesIL)}")
    # print(f"Distance totale parcourue insertion loin : {cout(listeVillesIL)} km\n\n")