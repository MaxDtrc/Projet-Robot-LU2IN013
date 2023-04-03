from math import pi, sqrt
from .position_balise import getPosBalise
from PIL import Image
from random import randint


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
    
    def getBalisePosition(self):
        """
        Retourne la position x de la balise sur l'image captée par la camera
        """
        img = self._r.get_image()
        
        #CONVERSION DE l'IMAGE ET APPEL DE LA FONCTION RENVOYANT LA POSITION DE LA BALISE
        im = Image.fromarray(img)

        im.save("camera.png")

        return getPosBalise()

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

    def dessine(self, b:bool):
        """
        change afficherTrace en b
        """
        self._s._afficherTrace=b

    def getBalisePosition(self):
        """
        Retourne la position x de la balise sur l'image captée par la camera
        """
        #print(self._a)
        if self._a != None:
            self._a.app.screenshot("camera.png", False)
        

        #CONVERSION DE l'IMAGE ET APPEL DE LA FONCTION RENVOYANT LA POSITION DE LA BALISE
        return getPosBalise()


    def stop(self):
        self._r.setVG(0)
        self._r.setVD(0)

    

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

        d = posRoues

        dG = d[0]/360 * diamRoue * pi
        dD = d[1]/360 * diamRoue * pi

        angle = (dD - dG)/(rayonRobot * 2)
        ancienAngle = self.lastStep
        if(angle != 0):
            #Test: remplacer la commande offeset_motor_encoder par une sauvegarde "manuelle"
            self.lastStep = angle
            #self.offset_motor_encoder(self.MOTOR_LEFT, self.read_encoders()[0])
            #self.offset_motor_encoder(self.MOTOR_RIGHT, self.read_encoders()[1])

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
        #Test: remplacer la commande offeset_motor_encoder par une sauvegarde "manuelle"
        self.lastStep = distance
        #self.offset_motor_encoder(self.MOTOR_LEFT, self.read_encoders()[0])
        #self.offset_motor_encoder(self.MOTOR_RIGHT, self.read_encoders()[1])

        return distance - ancienneDistance
    
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
    


class Variables(Decorator):
    def __init__(self, ctrl):
        self._variables = dict()
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
                    self._variables["capteur_distance"] = self.getDistance()
                if(vars[i] == "capteur_balise"):
                    self._variables["capteur_balise"] = self.getBalisePosition()
                if(vars[i] == "random"):
                    self._variables["random"] = randint(0, 10000000)

                #Si on a la variable drawStop dans le fichier.ia on lance 
                if(vars[i] == "drawStop"):
                    self.dessine(False) 
                #Si on a la variable drawStart dans le fichier.ia on lance 
                if(vars[i] == "drawStart"):
                    self.dessine(True)

                #Si on a la variable getSignal dans le fichier.ia on lance
                if(vars[i] == "getSignal"):
                    self._variables["getSignal"] = self.getSignal()

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

    def printVariable(self, args):
        """
        Fonction permettant d'afficher une variable dans la console
        
        :param args: arguments du print
        """
        args = args.copy()
        self.substituerVariables(args)
        print(eval(" ".join(args)))



