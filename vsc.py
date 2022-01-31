import math


class Ville:
    def __init__(self, num, nom, x, y):
        self.num = num
        self.nom = nom
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def __str__(self):
        return f"Villes : {self.num} {self.nom} {self.x} {self.y}"


f = open("instances/top80.txt", "r")
lines = f.readlines()
listeVilles = []
r = 6371

for x in lines:
    ville = x.split(" ")
    v = Ville(ville[0], ville[1], ville[2], ville[3])
    listeVilles.append(v)


def afficheVilles(liste):
    for x in liste:
        print(x)


def calcDistance(ville1, ville2):
    return abs(r*math.acos((math.sin(ville1.getX())*math.sin(ville2.getX())) + (math.cos(ville1.getY())*math.cos(ville2.getY())*math.cos(ville1.getX() - ville2.getX()))))


afficheVilles(listeVilles)
