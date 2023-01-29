import math
from Robot import Robot
from Obstacle import Obstacle
import numpy as np

class ObstacleCarre(Obstacle): 
    """
    Classe héritant de la classe Obstacle et représentant un obstacle carré
    """
    
    def __init__(self, nom: str, posX: float, posY: float, longueur: float):
        """
        Constructeur de la classe ObstacleCarré

        Paramètres:
        nom -> nom de l'obstacle
        posX -> position x du centre de l'obstacle 
        posY -> position y du centre de l'obstacle
        longueur -> longueur des côtés de l'obstacle
        """
        Obstacle.__init__(self, nom, posX, posY)
        self._longueur = longueur

        
    def testCrash(self, robot : Robot):
        """
    	Méthode qui détermine si le robot est en collision avec un obstacle carré
    	Renvoie 1 si crash, 0 sinon
    	#Marge d erreur de 0.2
    	"""

        #Coordonnées du robot
        p3 = np.array([robot.getX(), robot.getY()])

        #Obtention des coins de l'obstacle
        c1 = np.array([self._posX - self._longueur/2, self._posY - self._longueur/2])
        c2 = np.array([self._posX + self._longueur/2, self._posY - self._longueur/2])
        c3 = np.array([self._posX + self._longueur/2, self._posY + self._longueur/2])
        c4 = np.array([self._posX - self._longueur/2, self._posY + self._longueur/2])


        #Test avec chaque côté
        for (p1, p2) in [(c1, c2), (c2, c3), (c3, c4), (c4, c1)]:
            #Projection
            t = max(0, min(1, np.sum((p3 - p1) * (p2 - p1)) / np.sum((p1 - p2)**2)))
            projection = p1 + t * (p2 - p1)

            if math.sqrt((projection[0] - p3[0])** 2 + (projection[1] - p3[0])**2) < robot.getRayon() + 0.2:
                return 1

        
        return 0

    def estDedans(self, x : int, y : int):
        """
        Méthode abstraite qui détermine si le point de coordonnée (x, y) se trouve dans la surface de l'obstacle

        Paramètres:
        x -> coordonnée X
        y -> coordonnée Y
        """
        if self._posX - self._longueur < x < self._posX + self._longueur and self._posY - self._longueur < y < self._posY + self._longueur:
            return True
        else:
            return False