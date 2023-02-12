from math import cos, sin, radians, degrees, sqrt, pi
from abc import ABC, abstractmethod
from threading import Thread
import time

class Robot(Thread):
    """
    Classe représentant un robot
    """

    #Constructeur
    def __init__(self, nom: str, posX: float, posY: float, angle: float, t: float, r: float = 10, vG: float = 0, vD: float = 0, vMax: float = 10, dT: float = 0.1):
        """
        Constructeur de la classe Robot

        :param nom: nom du robot
        :param posX: position x du robot
        :param posY: position y du robot
        :param angle: orientation du robot (en degrés)
        :param t: diamètre des roues (en cm)
        :param r: rayon du robot
        :param vitesseMax: vitesse maximum des roues (en degrés de rotation par seconde)
        """
        super(Robot, self).__init__()
        self._dT = dT
        self._nom = nom
        self._posX = posX
        self._posY = posY
        self._rayon = r
        self._angle = radians(angle)
        self._tailleRoues = t
        self._vitesseGauche = vG
        self._vitesseDroite = vD
        self._vitesseMax = vMax

    def run(self):
        while True:
            self.actualiser()
            time.sleep(self._dT)

    #Getters
    @property
    def position(self):
        """
        :returns: tuple contenant la position (x, y) du robot
        """
        return (self._posX, self._posY)

    @property
    def x(self):
        """
        :returns: la position x du robot
        """
        return self._posX
    
    @property
    def y(self):
        """
        :returns: la position y du robot
        """
        return self._posY

    @property
    def nom(self):
        """
        :returns: le nom du robot
        """
        return self._nom

    @property
    def angle(self):
        """
        :returns: l'angle d'orientation du robot (en degrés)
        """
        return self._angle

    @property
    def rayon(self):
        """
        :returns: le rayon du robot
        """
        return self._rayon


    def getPosRoueGauche(self):
        """
        :returns: un tuple contenant la position absolue de la roue gauche
        """
        return (cos(self._angle + pi/2) * self._rayon + self._posX, sin(self._angle + pi/2) * self._rayon + self._posY)


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
        return (cos(self._angle - pi/2) * self._rayon + self._posX, sin(self._angle - pi/2) * self._rayon + self._posY)


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

    @property
    def vitesseGauche(self):
        """
        :returns: la vitesse de la roue gauche (en degrés de rotation par seconde)
        """
        return self._vitesseGauche
    
    @vitesseGauche.setter
    def vitesseGauche(self, v: float):
        """
        Actualise la vitesse de la roue gauche

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien
        """
        if(v > self._vitesseMax):
            self._vitesseGauche = self._vitesseMax
        elif(v < -self._vitesseMax):
            self._vitesseGauche = -self._vitesseMax
        else:
            self._vitesseGauche = v

    @property
    def vitesseDroite(self):
        """
        :returns: la vitesse de la roue droite (en degrés de rotation par seconde)
        """
        return self._vitesseDroite

    @vitesseDroite.setter
    def vitesseDroite(self, v: float):
        """
        Actualise la vitesse de la roue droite

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien
        """
        if(v > self._vitesseMax):
            self._vitesseDroite = self._vitesseMax
        elif(v < -self._vitesseMax):
            self._vitesseDroite = -self._vitesseMax
        else:
            self._vitesseDroite = v

    @property
    def vitesse(self):
        """
        :returns: la vitesse du robot sous la forme d'un tuple (vitesse roue gauche, vitesse roue droite, en degrés de rotation par seconde)
        """
        return (self._vitesseGauche, self._vitesseDroite)
    
    @vitesse.setter
    def vitesse(self, v: float):
        """
        Actualise la vitesse des deux roues

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien, changement in place
        """
        self.vitesseDroite = v
        self.vitesseGauche = v
    
    def getInfo(self):
        """
        :returns: les informations sur le robot sous forme  de string
        """
        return ("VitG: "+str(format(self._vitesseGauche,'.2f'))+"\tVitD: "+str(format(self._vitesseDroite,'.2f'))+"\tAngle: "+str(format(self._angle,'.2f')))

    #Contrôle du robot
    def actualiser(self):
        """
        Actualise la position et l'angle du robot selon le temps dT écoulé depuis la dernière actualisation

        :param dT: différence de temps (en seconde)
        :returns: rien, changement in place
        """
        #Calcul de la vitesse en cm/s du robot
        vG = self._vitesseGauche/360.0 * pi * self._tailleRoues
        vD = self._vitesseDroite/360.0 * pi * self._tailleRoues

        #Mise à jour de ses coordonnées (déplacement autour du centre de rotation du robot)
        self._posX += ((vG + vD)/2) * cos(self._angle) * self._dT
        self._posY -= ((vG + vD)/2) * sin(self._angle) * self._dT

        #Mise à jour de l'angle
        self._angle += (vD - vG)/(self._rayon * 2) * self._dT


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

    @property   
    def nom(self):
        """
        :returns: le nom de l'obstacle
        """
        return self._nom
  
    def getPosition(self):
        """
        :returns: un tuple contenant la position (x, y) de l'obstacle
        """
        return (self._posX, self._posY)

    def setPosition(self, pX : float, pY: float):
        """
        Modifie la position d'un obstacle

        :param pX: nouvelle position x du robot
        :param pY: nouvelle position y du robot
        :returns: rien, changement in place
        """
        self._posX = pX
        self._posY = pY

    @property
    def x(self):
        """
        :returns: la position x du centre de l'obstacle
        """
        return self._posX

    @property
    def y(self):
        """
        :returns: la position y du centre de l'obstacle
        """
        return self._posY
        
    



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

    @property
    def size(self):
        """
        :returns: un tuple correspondant à la taille du terrain (sizeX, sizeY)
        """
        return (self._sizeX, self._sizeY)

    @property
    def sizeX(self):
        """
        :returns: la taille X du terrain
        """
        return self._sizeX

    @property
    def sizeY(self):
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
        :param largeur: largeur des côtés de l'obstacle
        """
        Obstacle.__init__(self, nom, posX, posY)
        self._longueur = longueur
        self._largeur = largeur

    @property
    def longueur(self):
        """
        :returns: la longueur du rectangle
        """
        return self._longueur

    @property
    def largeur(self):
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

        x = robot.x
        y = robot.y

        #Calcul des distances x et y entre le centre du robot et le rectangle
        dx = abs(self._posX - x) - (self._longueur * 0.5)
        dy = abs(self._posY - y) - (self._largeur * 0.5)

        #On vérifie si ces distances sont plus petites que le rayon du robot (avec une marge d'erreur de 0.2)
        if sqrt((dx * (dx > 0)) ** 2 + (dy * (dy > 0)) ** 2) - robot.rayon < 0.2:
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

    @property
    def rayon(self):
        return self._rayon

        
    def testCrash(self, robot : Robot):
        """
    	Méthode qui détermine si le robot est en collision avec un obstacle rectangulaire
        #Marge d erreur de 0.2

        :param robot: robot sur lequel s'applique le test du crash avec un obstacle
    	:returns: 1 si crash, 0 sinon
    	"""

        posXRobot = robot.x
        posYRobot = robot.y
        rayonRobot = robot.rayon

        #Calcul de la distance entre le centre du robot et le centre du cercle
        distance = sqrt(pow((self._posX - posXRobot), 2) + pow((self._posY - posYRobot), 2))

        #On vérifie si cette distance est inférieure à la somme des deux rayons (avec une marge d'erreur de 0.2)
        return (distance - rayonRobot - self._rayon <= 0.2) 

    def estDedans(self, x: int, y: int):
        """
        Méthode qui détermine si le point de coordonnée (x, y) se trouve dans la surface de l'obstacle

        :param x: coordonnée X
        :param y: coordonnée Y
        :returns: True si le point (x,y) se trouve dans l'obstacle
        """
        return sqrt((self._posX - x)**2 + (self._posY - y)**2) < self._rayon
