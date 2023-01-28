import math
from Robot import Robot

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
    
        
