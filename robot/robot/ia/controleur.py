from math import pi

class implemSimulation:
    
    def __init__(self, robot, simulation):
        self._r = robot
        self._s = simulation

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

        :returns: la distance entre le robot et l'obstacle
        """
        return self._s.getDistanceFromRobot(self._r)

    def getDecalage(self):
        return self._r.getDecalage()


        

class implemVraiVie:
    def __init__(self, robot):
        self._r = robot

    def setVitesseGauche(self, v: float):
        """
        Set la vitesse de la roue gauche

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien
        """
        self._r.set_motor_dps(1, v)

    
    def setVitesseDroite(self, v: float):
        """
        Set la vitesse de la roue droite

        :param v: vitesse (en degrés de rotation par seconde)
        :returns: rien
        """
        self._r.set_motor_dps(2, v)

    def getDistance(self):
        """
        Retourne la distance entre le robot et l'obstacle

        :returns: la distance entre le robot et l'obstacle
        """
        return self._r.get_distance()
    
    def getDecalage(self):
        pass
        #A DEFINIR

class controleur:
    def __init__(self, implementation = None):
        """
        Initialisation du controleur

        :param implementation : l'implementation sur laquelle on va lancer le code (simulation ou dans la vraie vie)
        """

        self._imp = implementation

    def changerImplementation(self, newImp):
        """
        Change l'implementation courante

        :param newImp : l'implementation a mettre a la place de la courante
        """

        self._imp = newImp

    def __getattr__(self, name):
        return getattr(self._imp, name)


class Decorator:
    def __init__(self, robot):
        self.robot = robot
    def __getattr__(self, attr):
        return getattr(self.robot, attr)

class GetDecalageSim(Decorator):
    def __init__(self, robot):
        Decorator.__init__(self, robot)

    def __getattr__(self, name):
        return getattr(self.robot, name)

    def getDecalage(self):
        """
        Renvoi le décalage de l'angle du robot depuis le dernier appel de la fonction et le remet à 0

        :returns: le décalage de l'angle du robot depuis le dernier appel
        """
        res = self._angle - self._decalageA
        self._decalageA = self._angle
        return res

class GetDecalageReel(Decorator):
    def __init__(self, robot):
        Decorator.__init__(self, robot)
        self._decalage = (0, 0)

    def __getattr__(self, name):
        return getattr(self.robot, name)

    def getDecalage(self):
        """
        Renvoi le décalage de l'angle du robot depuis le dernier appel de la fonction et le remet à 0

        :returns: le décalage de l'angle du robot depuis le dernier appel
        """

        diamRoue = 6.65
        rayonRobot = 5.85

        posRoues = self.get_motor_position()

        d = posRoues - self._decalage
        self._decalage = posRoues

        dG = d[0] * diamRoue * pi
        dD = d[1] * diamRoue * pi

        angle = (dD - dG)/(rayonRobot * 2) * self._dT

        return angle