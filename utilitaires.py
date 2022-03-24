import random
import math
from ville import Ville
r=6371


def afficheVilles(liste):
    for x in liste:
        print(x)


def calculDistance(ville1, ville2):

    y1 = ville1.getY()
    y2 = ville2.getY()
    
    x1 = ville1.getX()
    x2 = ville2.getX()
    
    return  abs(r*math.acos((math.sin(y1)*math.sin(y2)) + (math.cos(y1)*math.cos(y2)*math.cos(x1-x2))))


def d(ville1, ville2):

    y1 = ville1.getY()
    y2 = ville2.getY()
    
    x1 = ville1.getX()
    x2 = ville2.getX()
    
    return  abs(r*math.acos((math.sin(y1)*math.sin(y2)) + (math.cos(y1)*math.cos(y2)*math.cos(x1-x2))))

def tourAleatoire(listeVA):
    random.shuffle(listeVA)
    return listeVA


def afficheTour(listeVT):
    liste = []
    for x in listeVT:
        liste.append(x.getNum())
    return liste


def cout(listeVillesC):
    distance = 0.00

    for i in range(len(listeVillesC)-1):
        distance += calculDistance(listeVillesC[i], listeVillesC[i+1])
    distance += calculDistance(listeVillesC[0], listeVillesC[-1])
    return distance


def plus_proche(listeVP, ville1):
    if(ville1 in listeVP):
        listeVP.pop(listeVP.index(ville1))

    listeDistances = []

    for v in listeVP:
        listeDistances.append([calculDistance(ville1, v), str(v)])
    
    dist, ville2 = listeDistances[listeDistances.index(min(listeDistances))]
    ville2 = ville2.split(" ")
    ville2 = Ville(ville2[0], ville2[1], ville2[2], ville2[3])
    return dist, ville2


def plus_loin(listeVL, ville1):
    listeDistances = []

    for x in listeVL:
        if(x != ville1):
            listeDistances.append([calculDistance(ville1, x), str(x)])

    dist, ville2 = listeDistances[listeDistances.index(max(listeDistances))]
    
    ville2 = ville2.split(" ")
    ville2 = Ville(ville2[0], ville2[1], ville2[2], ville2[3])
    return dist, ville1, ville2



def get_villes_plus_eloignees(listeVPE):
    liste_plus_loin = []
    for ville in listeVPE:
        liste_plus_loin.append(plus_loin(listeVPE, ville))
    
    liste_distances = []
    for x in liste_plus_loin:
        liste_distances.append(x[0])

    distance, ville1, ville2  = liste_plus_loin[liste_distances.index(max(liste_distances))]

    return [ville1, ville2]


def fromLatLong2pixels(coords, listeVLL2P, largeur, hauteur):

    minLat = float(coords.getLat())
    minLong = float(coords.getLong())

    maxLat = float(coords.getLat())
    maxLong = float(coords.getLong())

    for v in listeVLL2P:
        longitude = float(v.getLong())
        latitude = float(v.getLat())
        
        if(longitude < minLong):
            minLong = longitude
        if(longitude > maxLong):
            maxLong = longitude
        
        if(latitude < minLat):
            minLat = latitude
        if(latitude > maxLat):
            maxLat = latitude

    if (not minLat <= coords.getLat() <= maxLat) or (not minLong <= coords.getLong() <= maxLong):
        return None
    else:
        deltaLat = coords.getLat() - minLat
        deltaLong= coords.getLong()- minLong

        geoWidth = maxLat - minLat
        geoHeight= maxLong - minLong

        latRatio = deltaLat / geoWidth
        longRatio= deltaLong/ geoHeight

        x = latRatio * largeur
        y = longRatio * hauteur

        return x,y