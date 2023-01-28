import math
from Robot import Robot

class ObstacleRond(Obstacle): 
    """
    Classe héritant de la classe Obstacle et représentant un obstacle rond
    """
    
    def __init__(self, nom: str, posX: float, posY: float, rayon: float):
        """
        Constructeur de la classe ObstacleRond

        Paramètres:
        nom -> nom de l'obstacle
        posX -> position x du centre de l'obstacle 
        posY -> position y du centre de l'obstacle
        rayon -> rayon de l'obstacle
        """
        Obstacle.__init__(self, nom, posX, posY)
        self._rayon = rayon

        
    def testCrash(self, robot : Robot):
        """
    	Méthode qui détermine si le robot est en collision avec un obstacle rond
    	Renvoie 1 si crash, 0 sinon
    	#Marge d erreur de 0.2
    	"""
    	posXRobot = robot.getX()
    	posYRobot = robot.getY()
    	rayonRobot = robot.getRayon()
    	distance = sqrt(pow((self._posX - posXRobot), 2) + pow((self._posY - posYRobot), 2))
    	if (distance-rayonRobot-self._rayon <= 0.2): 
    		return 1
    	else:
    		return 0
        
