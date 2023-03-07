from math import pi, sqrt
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

        :returns: la distance entre le robot et l'obstacle (en cm)
        """
        return self._s.getDistanceFromRobot(self._r)

    def reset(self):
        pass

    

    def __getattr__(self, name):
        return getattr(self._r, name)

        

class implemVraiVie:
    def __init__(self, robot):
        self._r = robot

        #Reset de l'origine de la position
        self.offset_motor_encoder(self.MOTOR_LEFT, self.read_encoders()[0])
        self.offset_motor_encoder(self.MOTOR_RIGHT, self.read_encoders()[1])

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

        :returns: la distance entre le robot et l'obstacle (en cm)
        """
        return self._r.get_distance() / 10

    def reset(self):
        self.offset_motor_encoder(self.MOTOR_LEFT, self.read_encoders()[0])
        self.offset_motor_encoder(self.MOTOR_RIGHT, self.read_encoders()[1])

    def __getattr__(self, name):
        return getattr(self._r, name)
    

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

    def stop_ia_thread(self):
        self.running = False
        self.setVitesseGauche(0)
        self.setVitesseDroite(0)

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


class GetDecalageReel(Decorator):
    def __init__(self, robot):
        Decorator.__init__(self, robot)

    def __getattr__(self, name):
        return getattr(self.robot, name)

    def getDecalageAngle(self):
        """
        Renvoi le décalage de l'angle du robot depuis le dernier appel de la fonction et le remet à 0

        :returns: le décalage de l'angle du robot depuis le dernier appel
        """

        diamRoue = self.WHEEL_DIAMETER/10
        rayonRobot = self.WHEEL_BASE_WIDTH/20

        posRoues = self.get_motor_position()

        d = posRoues()

        dG = d[0]/360 * diamRoue * pi
        dD = d[1]/360 * diamRoue * pi

        angle = (dD - dG)/(rayonRobot * 2)

        return angle

    def getDistanceParcourue(self):
        """
        Renvoi la distance parcourue par le robot

        :returns: la distance parcourue par le robot
        """

        diamRoue = 6.65
        posRoues = self.get_motor_position()

        d = (posRoues[0] + posRoues[1])/2

        #Reset de l'origine de la pos
        self.offset_motor_encoder(self.MOTOR_LEFT, self.read_encoders()[0])
        self.offset_motor_encoder(self.MOTOR_RIGHT, self.read_encoders()[1])

        return d/360 * diamRoue * pi 