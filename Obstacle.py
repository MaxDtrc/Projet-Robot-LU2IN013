from math import cos, sin, radians, degrees
from Terrain import Terrain
from Robot import Robot
from abc import ABC, abstractmethod

class Obstacle(ABC): 
    """
    Classe abstraite représentant un obstacle
    """
    
    def __init__(self, nom: str, posX: float, posY: float):
        """
        Constructeur de la classe Obstacle

        Paramètres:
        nom -> nom de l'obstacle
        posX -> position x du centre de l'obstacle 
        posY -> position y du centre de l'obstacle
        """
        self._nom = nom
        self._posX = posX
        self._posY = posY

        
    @abstractmethod  
    def testCrash(self, robot : Robot):
    	"""
    	Méthode abstraite qui détermine si le robot est en collision avec un obstacle
    	"""
        pass
        
    def getNom(self):
    	"""
    	Renvoie le nom de l'obstacle"
    	"""
    	return self._nom
  

    def getPosition(self):
        """
        Renvoie un tuple contenant la position (x, y) de l'obstacle
        """
        return (self._posX, self._posY)

    def getX(self):
        """
        Renvoie la position x du centre de l'obstacle
        """
        return self._posX
    
    def getY(self):
        """
        Renvoie la position y du centre de l'obstacle
        """
        return self._posY
        
    def setPosition(self, pX : float, pY: float):
    	"""
    	Modifie la position d'un obstacle
    	"""
    	self._posX = pX
        self._posY = pY

