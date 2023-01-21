from math import cos, sin, radians

class Robot:
    """
    Classe représentant un robot
    """

    def __init__(self, nom: str, posX: float, posY: float, angle: float):
        """
        Constructeur de la classe Robot

        Paramètres:
        nom -> Nom du robot
        posX -> position x du robot
        posY -> position y du robot
        angle -> orientation du robot (en degré)
        """
        self.nom = nom
        self.posX = posX
        self.posY = posY
        self.angle = angle

    def avancer(self, distance: float):
        """
        Fait avancer le robot dans sa direction d'un certain nombre de centimètres
        
        Paramètres:
        distance -> Distance de l'avancée
        """
        self.posX = self.posX + distance * cos(radians(self.angle))
        self.posY = self.posY + distance * sin(radians(self.angle))

    def tourner(self, angle: float):
        return None

    def getPosition(self):
        return None

    def getX(self):
        return None
    
    def getY(self):
        return None

    def getNom(self):
        return None

    def getAngle(self):
        return None

    def getDistanceFromRobot(self):
        return None

    def afficher(self, screen):
        return None