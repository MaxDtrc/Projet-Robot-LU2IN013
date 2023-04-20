from math import pi, sqrt
from .position_balise import getPosBalise
from random import randint
from threading import Thread

#Implementations
class implemVraiVie:
    def __init__(self, robot):
        self._r = robot

        #Reset de l'origine de la position
        self.offset_motor_encoder(self.MOTOR_LEFT, self.read_encoders()[0])
        self.offset_motor_encoder(self.MOTOR_RIGHT, self.read_encoders()[1])

        #Lancement de la camera
        self.start_recording()

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
    
    def getBalisePosition(self):
        """
        Retourne la position x de la balise sur l'image captée par la camera
        """

        return getPosBalise(self._r.get_image())
    
    def setCerveau(self, angle: int):
        """
        Tourne la camera du robot
        
        :param angle: angle de rotation (de 0 à 180)
        """
        self.servo_rotate(angle)

    def stop(self):
        self._r.set_motor_dps(1, 0)
        self._r.set_motor_dps(2, 0)

    def __getattr__(self, name):
        return getattr(self._r, name)
    

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
        if self._a != None and self._a.app.lastImage is not None:
            return getPosBalise(self._a.app.lastImage)
        else:
            return -1
        
    def setCerveau(self, angle: int):
        """
        Tourne la camera du robot
        
        :param angle: angle de rotation (de 0 à 180)
        """
        self._r.setAngleCam(angle)


    def stop(self):
        self._r.setVG(0)
        self._r.setVD(0)

    

    def __getattr__(self, name):
        return getattr(self._r, name)
    
#Classe controleur "de base"
class controleur:
    def __init__(self, implementation = None):
        """
        Initialisation du controleur

        :param implementation : l'implementation sur laquelle on va lancer le code (simulation ou dans la vraie vie)
        """

        self._imp = implementation
        if implementation is not None:
            self._capteurs = Capteurs(implementation)

    def changerImplementation(self, newImp):
        """
        Change l'implementation courante

        :param newImp : l'implementation a mettre a la place de la courante
        """
        self._imp = newImp
        self._capteurs = Capteurs(newImp)

    def stop_ia_thread(self):
        self.running = False
        self.setVitesseGauche(0)
        self.setVitesseDroite(0)

    def __getattr__(self, name):
        return getattr(self._imp, name)


#Décorateurs de la classe Robot
class Decorator:
    def __init__(self, robot):
        self.robot = robot
    def __getattr__(self, attr):
        return getattr(self.robot, attr)

class GetDecalage(Decorator):
    def __init__(self, robot):
        Decorator.__init__(self, robot)
        self.lastStep = 0

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

        d = posRoues

        dG = d[0]/360 * diamRoue * pi
        dD = d[1]/360 * diamRoue * pi

        angle = (dD - dG)/(rayonRobot * 2)

        ancienAngle = self.lastStep
        if angle - ancienAngle != 0:
            self.lastStep = angle

        return angle - ancienAngle

    def getDistanceParcourue(self):
        """
        Renvoi la distance parcourue par le robot

        :returns: la distance parcourue par le robot
        """

        diamRoue = self.WHEEL_DIAMETER/10
        posRoues = self.get_motor_position()

        d = (posRoues[0] + posRoues[1])/2
        distance = d/360 * diamRoue * pi
        ancienneDistance = self.lastStep

        #Reset de l'origine de la pos
        if distance - ancienneDistance != 0:
            self.lastStep = distance


        return distance - ancienneDistance
    

class Variables(Decorator):
    def __init__(self, ctrl):
        #Création du dictionnaire avec quelques constantes
        self._variables = {"true": True, "false": False, "null": None, "capteurs_background": False}

        Decorator.__init__(self, ctrl)

    def getVar(self, nom):
        return self._variables[nom]
    
    def setVar(self, nom, val):
        self._variables[nom] = val

    def substituerVariables(self, vars):
        """
        Fonctions auxiliaire permettant de remplacer les variables par leur valeurs
        """
        for i in range(len(vars)):
            try:
                #L'élément est une valeur
                parsed = float(vars[i])
            except:
                #Variables custom
                if(vars[i] == "capteur_distance"):
                    self._variables["capteur_distance"] = self.getDistance() if not self._variables["capteurs_background"] else self._capteurs.capteurDistance
                if(vars[i] == "capteur_balise"):
                    self._variables["capteur_balise"] = self.getBalisePosition() if not self._variables["capteurs_background"] else self._capteurs.capteurBalise
                if(vars[i] == "random"):
                    self._variables["random"] = randint(0, 10000000)

                #On substitue la variable à sa valeur
                if(vars[i] not in ['(', ')', '==', '!=', '<', '>', '<=', '>=', '+', '-', '/', '*', '%', '//', "and", "or"]):
                    vars[i] = str(self._variables[vars[i]])

    def evaluerCondition(self, args):
        """
        Fonction évaluant la condition passée en paramètres
        
        :param args: arguments de la condition
        :returns: True si la condition est vérifiée, False sinon
        """
        args = args.copy()
        self.substituerVariables(args)

        #Si un des arguments et Null -> la condition est toujours fausse
        return(eval(" ".join(args)))
    
    def affecterValeur(self, args):
        """
        Fonction permettant d'affecter une valeur à une variable

        :param args: arguments de l'affectation
        """
        varAChanger = args[0]
        args = args.copy()[2:]
        self.substituerVariables(args)
        self._variables[varAChanger] = eval(" ".join(args))

        #Lancement/Arrêt des capteurs en arrière plan
        if self._variables["capteurs_background"] and not self._capteurs.running:
            self._capteurs.start()

    def printVariable(self, args):
        """
        Fonction permettant d'afficher une variable dans la console
        
        :param args: arguments du print
        """
        args = args.copy()
        self.substituerVariables(args)
        print(eval(" ".join(args)))


class Capteurs(Thread): 
    """
    Classe permettant d'utiliser les capteurs en arrière plan
    """

    def __init__(self, implementation):
        """
        Constructeur de la classe Capteurs

        :param implementation: implementation (réelle ou simulée) du robot
        """
        super(Capteurs, self).__init__()
        self.implem = implementation
        self.capteurBalise = None
        self.capteurDistance = None
        self.running = False

    def run(self):
        self.running = True
        while(self.running):
            self.capteurDistance = self.implem.getDistance()
            self.capteurBalise = self.implem.getBalisePosition()

            #print("capteurDistance:", self.capteurDistance, ", capteurBalise:", self.capteurBalise)
    
    def stop(self):
        self.running = False



