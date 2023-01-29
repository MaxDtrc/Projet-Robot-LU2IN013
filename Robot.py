from math import cos, sin, radians, degrees
from Terrain import Terrain

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
        
    #Capteur de distance
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
            #Detection des bords du terrain
            if(abs(posRayon[0]) >= terrain.getSizeX()/2 or abs(posRayon[1]) >= terrain.getSizeY()/2): #Le point (0,0) est au centre de l'écran donc normalement ça passe
                return distance

            #Detection des obstacles
            for o in terrain.getListeObstacles():
                if o.estDedans(posRayon[0], posRayon[1]):
                    return distance
            
            tickRayon = 0.1
            distance += tickRayon
            posRayon = (posRayon[0] + tickRayon * dirVect[0], posRayon[1] + tickRayon * dirVect[1])

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