from math import cos, sin, radians, degrees, sqrt
from abc import ABC, abstractmethod
import numpy as np

class Robot:
    """
    Classe représentant un robot
    """

    #Constructeur
    def __init__(self, nom: str, posX: float, posY: float, angle: float, r: float = 10, vMax: float = 10):
        """
        Constructeur de la classe Robot

        Paramètres:
        nom -> Nom du robot
        posX -> position x du robot
        posY -> position y du robot
        rayon -> rayon du robot
        angle -> orientation du robot (en degrés)
        vitesseGauche -> vitesse de la roue gauche
        vitesseDroite -> vitesse de la roue droite
        vitesseMax -> vitesse maximum des roues
        """
        self._nom = nom
        self._posX = posX
        self._posY = posY
        self._rayon = r
        self._angle = angle
        self._vitesseGauche = 0
        self._vitesseDroite = 0
        self._vitesseMax = vMax

    #Getters
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
        
    def getY(self):
        """
        Renvoie la position y du robot
        """
        return self._rayon

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

    def getRayon(self):
        """
        Renvoie le rayon du robot
        """
        return self._rayon

    def getPosRoueGauche(self):
        """
        Renvoie un tuple contenant la position absolue de la roue gauche
        """
        return (cos(radians(self._angle + 90)) * self._rayon + self._posX, sin(radians(self._angle + 90)) * self._rayon + self._posY)

    def getPosRoueGaucheX(self):
        """
        Renvoie la position X de la roue gauche
        """
        return self.getPosRoueGauche()[0]

    def getPosRoueGaucheY(self):
        """
        Renvoie la position Y de la roue gauche
        """
        return self.getPosRoueGauche()[1]

    def getPosRoueDroite(self):
        """
        Renvoie un tuple contenant la position absolue de la roue droite
        """
        return (cos(radians(self._angle - 90)) * self._rayon + self._posX, sin(radians(self._angle - 90)) * self._rayon + self._posY)

    def getPosRoueDroiteX(self):
        """
        Renvoie la position X de la roue droite
        """
        return self.getPosRoueDroite()[0]

    def getPosRoueDroiteY(self):
        """
        Renvoie la position Y de la roue droite
        """
        return self.getPosRoueDroite()[1]

    def getVitesseGauche(self):
        """
        Renvoie le vitesse de la roue gauche
        """
        return self._vitesseGauche

    def getVitesseDroite(self):
        """
        Renvoie la vitesse de la roue gauche
        """
        return self._vitesseDroite
        

    #Contrôle du robot
    def actualiser(self, dT: float):
        """
        Actualise la position et l'angle du robot selon le temps dT écoulé depuis la dernière actualisation

        Paramètres:
        dT -> différence de temps (en seconde)
        """
        a = radians(self._angle)
        self._posX += ((self._vitesseGauche + self._vitesseDroite)/2) * cos(a) * dT
        self._posY -= ((self._vitesseGauche + self._vitesseDroite)/2) * sin(a) * dT
        self._angle += degrees((self._vitesseDroite - self._vitesseGauche)/self._rayon * dT)

    def accelererGauche(self, v: float):
        """
        Augmente la vitesse de la roue gauche du robot

        Paramètres:
        v -> vitesse à ajouter
        """
        if(abs(self._vitesseGauche + v) > self._vitesseMax):
            self._vitesseGauche = self._vitesseMax
        elif((self._vitesseGauche + v) < -self._vitesseMax):
            self._vitesseGauche = -self._vitesseMax
        else:
            self._vitesseGauche = self._vitesseGauche + v

    def accelererDroite(self, v: float):
        """
        Augmente la vitesse de la roue droite du robot

        Paramètres:
        v -> vitesse à ajouter
        """
        if((self._vitesseDroite + v) > self._vitesseMax):
            self._vitesseDroite = self._vitesseMax
        elif((self._vitesseDroite + v) < -self._vitesseMax):
            self._vitesseDroite = -self._vitesseMax
        else:
            self._vitesseDroite = self._vitesseDroite + v

    def setVitesseDroite(self, v: float):
        """
        Actualise la vitesse de la roue droite

        Paramètres:
        v -> vitesse à ajouter
        """
        if(v > self._vitesseMax):
            self._vitesseDroite = self._vitesseMax
        elif(v < -self._vitesseMax):
            self._vitesseDroite = -self._vitesseMax
        else:
            self._vitesseDroite = v

    def setVitesseGauche(self, v: float):
        """
        Actualise la vitesse de la roue gauche

        Paramètres:
        v -> vitesse à ajouter
        """
        if(v > self._vitesseMax):
            self._vitesseGauche = self._vitesseMax
        elif(v < -self._vitesseMax):
            self._vitesseGauche = -self._vitesseMax
        else:
            self._vitesseGauche = v


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

    @abstractmethod
    def estDedans(self, x : int, y : int):
        """
        Méthode abstraite qui détermine si le point de coordonnée (x, y) se trouve dans la surface de l'obstacle
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



class Terrain:
    """
    Classe représentant un terrain
    """

    def __init__(self, sizeX: int, sizeY: int):
        """
        Constructeur de la classe
        
        Paramètres:
        sizeX -> taille X du terrain
        sizeY -> taille Y du terrain
        """
        self._sizeX = sizeX
        self._sizeY = sizeY
        self._listeObstacles = list()
    
    def getSize(self):
        """
        Renvoie un tuple correspondant à la taille du terrain (sizeX, sizeY)
        """
        return (self._sizeX, self._sizeY)

    def getSizeX(self):
        """
        Renvoie la taille X du terrain
        """
        return self._sizeX

    def getSizeY(self):
        """
        Renvoie la taille Y du terrain
        """
        return self._sizeY

    def addObstacle(self, obstacle : Obstacle):
        """
        Ajoute un obstacle à la liste des obstacles du terrain
        """

        self._listeObstacles.append(obstacle)

    def getListeObstacles(self):
        """
        Renvoie la liste des obstacles du terrain
        """
        return self._listeObstacles



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

            if sqrt((projection[0] - p3[0])** 2 + (projection[1] - p3[0])**2) < robot.getRayon() + 0.2:
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
        

