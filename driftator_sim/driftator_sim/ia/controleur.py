from math import pi, sqrt
from PIL import Image
import driftator


class implemSimulation:
    
    def __init__(self, robot, simulation, affichage3d = None):
        self._r = robot
        self._s = simulation
        self._a = affichage3d

    def setVitesseGauche(self, v: float):
        """
        Set la vitesse de la roue gauche

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien
        """
        #self._r.vitesseGauche = v
        self._r.setVG(v)

    
    def setVitesseDroite(self, v: float):
        """
        Set la vitesse de la roue droite

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien
        """
        #self._r.vitesseDroite = v
        self._r.setVD(v)

    def getDistance(self):
        """
        Retourne la distance entre le robot et l'obstacle

        :returns: la distance entre le robot et l'obstacle (en cm)
        """
        return self._s.getDistanceFromRobot(self._r)
    
    def set_a(self, a):
        self._a = a


    def getBalisePosition(self):
        """
        Retourne la position x de la balise sur l'image captée par la camera
        """
        #print(self._a)
        if self._a != None:
            self._a.app.screenshot("camera.png", False)
        

        #CONVERSION DE l'IMAGE ET APPEL DE LA FONCTION RENVOYANT LA POSITION DE LA BALISE
        return driftator.ia.getPosBalise()


    def reset(self):
        pass

    

    def __getattr__(self, name):
        return getattr(self._r, name)


class GetDecalageSim(driftator.ia.Decorator):
    def __init__(self, robot):
        driftator.ia.Decorator.__init__(self, robot)
        self._decalageA = 0 #dernier angle obtenu
        self._pos = (0, 0)

    def __getattr__(self, name):
        return getattr(self.robot, name)

    def getDecalageAngle(self):
        """
        Renvoi le décalage de l'angle du robot depuis le dernier appel de la fonction et le remet à 0

        :returns: le décalage de l'angle du robot depuis le dernier appel
        """
        res = self._angle - self._decalageA
        self._decalageA = self._angle
        return res

    def getDistanceParcourue(self):
        """
        Renvoi la distance parcourue par le robot

        :returns: la distance parcourue par le robot
        """

        newPos = (self.x, self.y)
        d = (newPos[0] - self._pos[0], newPos[1] - self._pos[1])
        self._pos = newPos

        dP = sqrt(d[0]**2 + d[1]**2)

        return dP