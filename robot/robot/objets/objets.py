from math import cos, sin, radians, degrees, sqrt, pi
from abc import ABC, abstractmethod
import numpy as np

class Robot:
    """
    Classe représentant un robot
    """

    #Constructeur
    def __init__(self, nom: str, posX: float, posY: float, angle: float, t: float, r: float = 10, vMax: float = 10):
        """
        Constructeur de la classe Robot

        :param nom: nom du robot
        :param posX: position x du robot
        :param posY: position y du robot
        :param rayon: rayon du robot
        :param angle: orientation du robot (en degrés)
        :param tailleRoue: diamètre des roues (en cm)
        :param vitesseGauche: vitesse de la roue gauche
        :param vitesseDroite: vitesse de la roue droite
        :param vitesseMax: vitesse maximum des roues
        """
        self._nom = nom
        self._posX = posX
        self._posY = posY
        self._rayon = r
        self._angle = angle
        self._tailleRoues = t
        self._vitesseGauche = 0
        self._vitesseDroite = 0
        self._vitesseMax = vMax

    #Getters
    def getPosition(self):
        """
        :returns: tuple contenant la position (x, y) du robot
        """
        return (self._posX, self._posY)

    def getX(self):
        """
        :returns: la position x du robot
        """
        return self._posX
    
    def getY(self):
        """
        :returns: la position y du robot
        """
        return self._posY

    def getNom(self):
        """
        :returns: le nom du robot
        """
        return self._nom
        
    def getAngle(self):
        """
        :returns: l'angle d'orientation du robot (en degrés)
        """
        return self._angle

    def getRayon(self):
        """
        :returns: le rayon du robot
        """
        return self._rayon

    def getPosRoueGauche(self):
        """
        :returns: un tuple contenant la position absolue de la roue gauche
        """
        return (cos(radians(self._angle + 90)) * self._rayon + self._posX, sin(radians(self._angle + 90)) * self._rayon + self._posY)

    def getPosRoueGaucheX(self):
        """
        :returns: la position X de la roue gauche
        """
        return self.getPosRoueGauche()[0]

    def getPosRoueGaucheY(self):
        """
        :returns: la position Y de la roue gauche
        """
        return self.getPosRoueGauche()[1]

    def getPosRoueDroite(self):
        """
        :returns: un tuple contenant la position absolue de la roue droite
        """
        return (cos(radians(self._angle - 90)) * self._rayon + self._posX, sin(radians(self._angle - 90)) * self._rayon + self._posY)

    def getPosRoueDroiteX(self):
        """
        :returns: la position X de la roue droite
        """
        return self.getPosRoueDroite()[0]

    def getPosRoueDroiteY(self):
        """
        :returns: la position Y de la roue droite
        """
        return self.getPosRoueDroite()[1]


    def getVitesseGauche(self):
        """
        :returns: la vitesse de la roue gauche
        """
        return self._vitesseGauche

    def getVitesseDroite(self):
        """
        :returns: la vitesse de la roue gauche
        """
        return self._vitesseDroite

    def getVitesse(self):
        """
        :returns: la vitesse du robot sous la forme d'un tuple (vitesse roue gauche, vitesse roue droite)
        """
        return (self._vitesseGauche, self._vitesseDroite)
    
    def getInfo(self):
        """
        :returns: les informations sur le robot sous forme  de string
        """
        return ("VitG: "+str(format(self.getVitesseGauche(),'.2f'))+"\tVitD: "+str(format(self.getVitesseDroite(),'.2f'))+"\tAngle: "+str(format(self.getAngle(),'.2f')))

    #Contrôle du robot
    def actualiser(self, dT: float):
        """
        Actualise la position et l'angle du robot selon le temps dT écoulé depuis la dernière actualisation

        :param dT: différence de temps (en seconde)
        :returns: rien, changement in place
        """
        a = radians(self._angle)
        self._posX += ((self._vitesseGauche + self._vitesseDroite)/2) * cos(a) * dT
        self._posY -= ((self._vitesseGauche + self._vitesseDroite)/2) * sin(a) * dT
        a+=(self._vitesseDroite - self._vitesseGauche)/self._rayon * dT
        self._angle = degrees(a)
        self._angle %= 360

    def setVitesseDroite(self, v: float):
        """
        Actualise la vitesse de la roue droite

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien, changement in place
        """
        dps = v/360 * pi * self._tailleRoues

        if(dps > self._vitesseMax):
            self._vitesseDroite = self._vitesseMax
        elif(dps < -self._vitesseMax):
            self._vitesseDroite = -self._vitesseMax
        else:
            self._vitesseDroite = dps

    def setVitesseGauche(self, v: float):
        """
        Actualise la vitesse de la roue gauche

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien, changement in place
        """
        dps = v/360 * pi * self._tailleRoues

        if(dps > self._vitesseMax):
            self._vitesseGauche = self._vitesseMax
        elif(dps < -self._vitesseMax):
            self._vitesseGauche = -self._vitesseMax
        else:
            self._vitesseGauche = dps

    def setVitesse(self, v: float):
        """
        Actualise la vitesse des deux roues

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien, changement in place
        """
        self.setVitesseDroite(v)
        self.setVitesseGauche(v)


class Obstacle(ABC): 
    """
    Classe abstraite représentant un obstacle
    """
    
    def __init__(self, nom: str, posX: float, posY: float):
        """
        Constructeur de la classe Obstacle

        :param nom: nom de l'obstacle
        :param posX: position x du centre de l'obstacle 
        :param posY: position y du centre de l'obstacle
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
        :returns: le nom de l'obstacle
        """
        return self._nom
  

    def getPosition(self):
        """
        :returns: un tuple contenant la position (x, y) de l'obstacle
        """
        return (self._posX, self._posY)

    def getX(self):
        """
        :returns: la position x du centre de l'obstacle
        """
        return self._posX
    
    def getY(self):
        """
        :returns: la position y du centre de l'obstacle
        """
        return self._posY
        
    def setPosition(self, pX : float, pY: float):
        """
        Modifie la position d'un obstacle

        :param pX: nouvelle position x du robot
        :param pY: nouvelle position y du robot
        :returns: rien, changement in place
        """
        self._posX = pX
        self._posY = pY



class Terrain:
    """
    Classe représentant un terrain
    """

    def __init__(self, sizeX: int, sizeY: int, obstaclesList : list = None):
        """
        Constructeur de la classe
        
        :param sizeX: taille X du terrain
        :param sizeY: taille Y du terrain
        """
        self._sizeX = sizeX
        self._sizeY = sizeY

        if obstaclesList is None : 
            self._listeObstacles = []
        else:
            self._listeObstacles = obstaclesList

    
    def getSize(self):
        """
        :returns: un tuple correspondant à la taille du terrain (sizeX, sizeY)
        """
        return (self._sizeX, self._sizeY)

    def getSizeX(self):
        """
        :returns: la taille X du terrain
        """
        return self._sizeX

    def getSizeY(self):
        """
        :returns: la taille Y du terrain
        """
        return self._sizeY

    def ajouterObstacle(self, obstacle : Obstacle):
        """
        Ajoute un obstacle à la liste des obstacles du terrain

        :param obstacle: l'obstacle à ajouter sur le terrain
        :returns: rien, changement in place
        """

        self._listeObstacles.append(obstacle)

    def getNombreObstacles(self):
        """
        :returns: le nombre d'obstacles sur le terrain
        """
        return len(self._listeObstacles)

    def getObstacle(self, index: int):
        """
        :param index: index de l'obstacle à renvoyer
        :returns: l'obstacle correspondant à l'index passé en paramètre dans le tableau des obstacles
        """
        return self._listeObstacles[index]



class ObstacleRectangle(Obstacle): 
    """
    Classe héritant de la classe Obstacle et représentant un obstacle rectangulaire
    """
    
    def __init__(self, nom: str, posX: float, posY: float, longueur: float, largeur: float):
        """
        Constructeur de la classe ObstacleRectangle

        :param nom: nom de l'obstacle
        :param posX: position x du centre de l'obstacle 
        :param posY: position y du centre de l'obstacle
        :param longueur: longueur des côtés de l'obstacle
        """
        Obstacle.__init__(self, nom, posX, posY)
        self._longueur = longueur
        self._largeur = largeur

    def getLongueur(self):
        """
        :returns: la longueur du rectangle
        """
        return self._longueur

    def getLargeur(self):
        """
        :returns: la largeur du rectangle
        """
        return self._largeur

        
    def testCrash(self, robot : Robot):
        """
    	Méthode qui détermine si le robot est en collision avec un obstacle rectangulaire
        #Marge d erreur de 0.2

        :param robot: robot sur lequel s'applique le test du crash avec un obstacle
    	:returns: 1 si crash, 0 sinon
    	"""

        x = robot.getX()
        y = robot.getY()

        dx = abs(self._posX - x) - (self._longueur * 0.5)
        dy = abs(self._posY - y) - (self._largeur * 0.5)
        if sqrt((dx * (dx > 0)) ** 2 + (dy * (dy > 0)) ** 2) - robot.getRayon() < 0.2:
            return 1
        else:
            return 0


    def estDedans(self, x : int, y : int):
        """
        Méthode qui détermine si le point de coordonnée (x, y) se trouve dans la surface de l'obstacle

        :param x: coordonnée X
        :param y: coordonnée Y
        :returns: True si le point (x,y) se trouve dans l'obstacle
        """
        if self._posX - self._longueur/2 <= x <= self._posX + self._longueur/2 and self._posY - self._largeur/2 <= y <= self._posY + self._largeur/2:
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

        :param nom: nom de l'obstacle
        :param posX: position x du centre de l'obstacle 
        :param posY: position y du centre de l'obstacle
        :param rayon: rayon de l'obstacle
        """
        Obstacle.__init__(self, nom, posX, posY)
        self._rayon = rayon

    def getRayon(self):
        return self._rayon

        
    def testCrash(self, robot : Robot):
        """
    	Méthode qui détermine si le robot est en collision avec un obstacle rectangulaire
        #Marge d erreur de 0.2

        :param robot: robot sur lequel s'applique le test du crash avec un obstacle
    	:returns: 1 si crash, 0 sinon
    	"""

        posXRobot = robot.getX()
        posYRobot = robot.getY()
        rayonRobot = robot.getRayon()
        distance = sqrt(pow((self._posX - posXRobot), 2) + pow((self._posY - posYRobot), 2))

        return (distance - rayonRobot - self._rayon <= 0.2) 

    def estDedans(self, x: int, y: int):
        """
        Méthode qui détermine si le point de coordonnée (x, y) se trouve dans la surface de l'obstacle

        :param x: coordonnée X
        :param y: coordonnée Y
        :returns: True si le point (x,y) se trouve dans l'obstacle
        """
        return sqrt((self._posX - x)**2 + (self._posY - y)**2) < self._rayon
