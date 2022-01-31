from dis import dis
import math
import random
from re import S
import time


class Ville:
    def __init__(self, num, nom, y, x):
        self.num = num
        self.nom = nom
        self.x = x
        self.y = y


    def getX(self):
        return math.radians(float(self.x))

    def getY(self):
        return math.radians(float(self.y))
    
    def getNom(self):
        return str(self.nom)
    
    def getNum(self):
        return int(self.num)

    def __str__(self):
        return f"{self.num} {self.nom} {self.y} {self.x}"
    
    def __eq__(self, other):
        return self.num == other.num and self.nom == other.nom

def afficheVilles(liste):
    for x in liste:
        print(x)

def calculDistance(ville1, ville2):

    y1 = ville1.getY()
    y2 = ville2.getY()
    
    x1 = ville1.getX()
    x2 = ville2.getX()
    
    return  float(abs(r*math.acos((math.sin(y1)*math.sin(y2)) + (math.cos(y1)*math.cos(y2)*math.cos(x1-x2)))))

def tourAleatoire(listeV):
    random.shuffle(listeV)

def afficheTour(listeV):
    liste = []
    for x in listeV:
        liste.append(x.getNum())
    return liste

def cout(listeVilles):
    distance = 0.00

    for i in range(len(listeVilles)-1):
        distance += calculDistance(listeVilles[i], listeVilles[i+1])
    distance += calculDistance(listeVilles[0], listeVilles[-1])
    return distance

def plus_proche_voisin(listeV, ville):
    t= []
    t.append(ville)
    

    while len(listeV) > 1:
        suivant = plus_proche(listeV, ville)[1]
        t.append(suivant)
        ville = suivant

    return t

def plus_proche(listeV, ville):
    if(ville in listeV):
        listeV.pop(listeV.index(ville))

    listeDistances = []

    for x in listeV:
        listeDistances.append([calculDistance(ville, x), str(x)])
    
    dist, ville = listeDistances[listeDistances.index(min(listeDistances))]
    ville = ville.split(" ")
    ville = Ville(ville[0], ville[1], ville[2], ville[3])
    return dist, ville

def plus_proche_voisin_ameliore():
    listeDistances = []

    for v in listeVillesCopie:
        listeV = listeVillesCopie.copy()
        tournee = plus_proche_voisin(listeV, v)
        listeDistances.append([cout(tournee), tournee])
    
    tournee_min = listeDistances[listeDistances.index(min(listeDistances))][1]

    return tournee_min

def plus_loin(listeV, ville):
    listeDistances = []

    for x in listeV:
        if(x != ville):
            listeDistances.append([calculDistance(ville, x), str(x)])

    dist, v = listeDistances[listeDistances.index(max(listeDistances))]
    
    v = v.split(" ")
    v = Ville(v[0], v[1], v[2], v[3])
    return dist, ville, v

def insertion_proche(listeV):
    liste_plus_loin = []
    for x in listeV:
        liste_plus_loin.append(plus_loin(listeV, x))
    
    liste_distances = []
    for x in liste_plus_loin:
        liste_distances.append(x[0])



    _, ville1, ville2  = liste_plus_loin[liste_distances.index(max(liste_distances))]

    t = [ville1, ville2]


    while len(listeV)>1:
        liste_distances = []

        for ville in t:
            liste_distances.append(plus_proche(listeV, ville))
            b = [i[0] for i in liste_distances]
        suivant = liste_distances[b.index(min(b))][1]
        t.append(suivant)
        listeV.pop(listeV.index(suivant))
    
    return t


if __name__ == "__main__":

    #============================================================#
    #Chargment des données#
    f = open("instances/top80.txt", "r")
    lines = f.readlines()
    listeVilles = []

    tourneeVilles = []
    r = 6371


    for x in lines:
        ville = x.split(" ")
        v = Ville(ville[0], ville[1], ville[2], ville[3])
        listeVilles.append(v)

    listeVillesCopie = listeVilles.copy()
    #============================================================#



    tournee_insertion_proche = insertion_proche(listeVillesCopie)


    print(cout(tournee_insertion_proche))



    # distanceTotaleOrdre = cout(listeVilles)
    # print(f"Distance totale parcourue ordre croissant: {distanceTotaleOrdre} km")
    # print(f"Chemin utilisé dans l'ordre : {afficheTour(listeVilles)}\n\n")

    # print(f"Ville la plus proche de {listeVilles[0].getNom()} : {str(plus_proche(listeVilles, listeVilles[0]))}")

    # tourAleatoire(listeVilles)
    # distanceTotale = cout(listeVilles)
    # print(f"Distance totale parcourue aléatoire: {distanceTotale} km")
    # print(f"Chemin utilisé aléatoire : {afficheTour(listeVilles)}")

    # tournee_glouton = plus_proche_voisin(listeVilles, listeVilles[0])
    # print(f"Chemin utilise dans glouton : {afficheTour(tournee_glouton)}")
    # print(f"Distance totale parcourue glouton : {cout(tournee_glouton)} km\n\n")


    # tournee_glouton_ameliore = plus_proche_voisin_ameliore()
    # print(f"Chemin utilise dans glouton ameliore : {afficheTour(tournee_glouton_ameliore)}")
    # print(f"Distance totale parcourue glouton ameliore: {cout(tournee_glouton_ameliore)} km\n\n")

