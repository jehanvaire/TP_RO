import math


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
    
    def getLat(self):
        return float(self.x)
    
    def getLong(self):
        return float(self.y)
    
    def getNom(self):
        return str(self.nom)
    
    def getNum(self):
        return int(self.num)

    def __str__(self):
        return f"{self.num} {self.nom} {self.y} {self.x}"
    
    def __eq__(self, other):
        return self.num == other.num and self.nom == other.nom

