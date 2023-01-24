from math import cos, sin, radians
from Terrain import Terrain

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
        angle -> orientation du robot (en degrés)
        """
        self._nom = nom
        self._posX = posX
        self._posY = posY
        self._angle = angle

    def avancer(self, distance: float):
        """
        Fait avancer le robot dans sa direction d'un certain nombre de centimètres
        
        Paramètres:
        distance -> Distance de l'avancée
        """
        self._posX = self._posX + distance * cos(radians(self._angle))
        self._posY = self._posY + distance * sin(radians(self._angle))

    def tourner(self, angle: float):
        """
        Effectue une rotation du robot d'un certain nombre de degrés
        
        Paramètres:
        angle -> Angle de la rotation (en degrés)
        """

        self._angle += angle

    def getPosition(self):
        """
        Renvoie un tuple contenant la position (x, y) du robot
        """
        return (self._posX, self._posY)

    def getX(self):
        """
        Renvoie la position x du robot
        """
        return self._posX
    
    def getY(self):
        """
        Renvoie la position y du robot
        """
        return self._posY

    def getNom(self):
        """
        Renvoie le nom du robot
        """
        return self._nom
        
    def getAngle(self):
        """
        Renvoie l'angle d'orientation du robot (en degrés)
        """
        return self._angle

    def getDistanceFromRobot(self, terrain: Terrain):
        """
        Renvoie la distance jusqu'au prochain mur
        
        Paramètres:
        terrain -> Terrain
        """

        dirVect = (cos(radians(self._angle)), sin(radians(self._angle)))
        posRayon = (self._posX, self._posY)
        distance = 0

        while distance < terrain.getSizeX() * terrain.getSizeY(): #Limite pour pas que le rayon n'avance à l'infini
            if(abs(posRayon[0]) >= terrain.getSizeX()/2 or abs(posRayon[1]) >= terrain.getSizeY()/2): #Le point (0,0) est au centre de l'écran donc normalement ça passe
                return distance
            
            tickRayon = 0.1
            distance += tickRayon
            posRayon = (posRayon[0] + tickRayon * dirVect[0], posRayon[1] + tickRayon * dirVect[1])

