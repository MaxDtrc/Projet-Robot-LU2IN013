from threading import Thread
import time
from math import pi, radians, degrees
from random import randint



class IA(Thread):
    """
    Classe représentant l'IA
    """
    def __init__(self, controleur, strat, dT):
        super(IA, self).__init__()
        self._controleur = controleur
        self.strategie = strat
        self._wait = dT

    def run(self):
        self.strategie.start()
        self._controleur.running = True
        while self._controleur.running:
            #Etape suivante
            self._lastTime = time.time()
            time.sleep(self._wait)
            self._dT = time.time() - self._lastTime
            self.step()

    def step(self):
        if not self.strategie.stop():
            self.strategie.step()
        else:
            self._controleur.stop()
            self._controleur.running = False





#IA de déplacement
class Avancer:
    """
    Classe représentant l'ia permettant d'avancer droit

    :param controleur: controleur du robot
    :param distance: distance (cm) dont le robot doit avancer
    :param v: vitesse (tour de roue/s)
    :param angle: angle de la trajectoire du robot (pourcentage de -100 à 100)
    """
    def __init__(self, controleur, distance, v, angle = 0):
        self._controleur = controleur
        self.d = distance
        self.a = angle
        self.v = v
        self.parcouru = 0

    def start(self):
        self._controleur.getDistanceParcourue() #Reinitialisation
        self.parcouru = 0

        #Substitution des variables
        self._vars = [self.d, self.a, self.v]
        self._controleur.substituerVariables(self._vars)
        self.distance = float(self._vars[0])
        self.angle = float(self._vars[1])
        self.vitesse = float(self._vars[2])

        self.avancer()

    def stop(self):
        #On avance tant qu'on n'est pas trop près d'un mur/qu'on n' a pas suffisement avancé
        return self.parcouru >= self.distance

    def step(self):
        #Calcul de la distance parcourue
        self.parcouru += abs(self._controleur.getDistanceParcourue())

        self.avancer()


    def avancer(self):
        #Avancer selon l'angle et la vitesse
        if self.angle <= 0:
            self._controleur.setVitesseGauche(self.vitesse * (1 + self.angle/100))
            self._controleur.setVitesseDroite(self.vitesse)
        else:
            self._controleur.setVitesseGauche(self.vitesse)
            self._controleur.setVitesseDroite(self.vitesse * (1 - self.angle/100))

class TournerSurPlace:
    """
    Classe représentant l'ia permettant de tourner à droite

    :param controleur: controleur du robot
    :param angle: angle (degré) de rotation
    :param v: vitesse (tour de roue/s)
    """
    def __init__(self, controleur, angle, v):
        self._controleur = controleur
        self.a = angle
        self.v = v
        self.parcouru = 0


    def start(self):
        self._controleur.getDecalageAngle()
        self.parcouru = 0

        #Substitution des variables
        self._vars = [self.a, self.v]
        self._controleur.substituerVariables(self._vars)

        self.angle = radians(float(self._vars[0]))
        self.vitesse = float(self._vars[1]) if self.angle >= 0 else -float(self._vars[1])


        self.avancer()

    def stop(self):
        #On tourne tant qu'on n'a pas dépassé l'angle
        return self.parcouru > abs(self.angle)
        
    def step(self):
        #Calcul de la distance parcourue
        self.parcouru += abs(self._controleur.getDecalageAngle())
        self.avancer()

    def avancer(self):
        self._controleur.setVitesseGauche(self.vitesse)
        self._controleur.setVitesseDroite(-self.vitesse)




#IA complexes
class IAIf:
    """
    Classe permettant de réaliser un "if"
    """
    def __init__(self, controleur, ia1, ia2, condition):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia1: ia à appeler si la condition est vérifiée
        :param ia2: ia à appeler si la condition n'est pas vérifiée
        :param condition: IACondition correspondant à la condition du if
        """
        self._controleur = controleur
        self._ia1 = ia1
        self._ia2 = ia2
        self._condition = condition

    def start(self):
        #Initialisation des 2 sous IA
        if self._controleur.evaluerCondition(self._condition):
            self._ia = self._ia1
        else:
            self._ia = self._ia2

        if(self._ia != None):
            self._ia.start()


    def stop(self):
        #Arrêt si l'une des deux IA est finie
        return self._ia == None or self._ia.stop()

    def step(self):
        self._ia.step()
    

#IA complexes
class IAAlterner:
    """
    Classe permettant de réaliser une ia conditionnelle (réalise un step d'une des deux IA selon la condition)
    """
    def __init__(self, controleur, ia1, ia2, condition):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia1: ia à appeler si la condition est vérifiée
        :param ia2: ia à appeler si la condition n'est pas vérifiée
        :param condition: IACondition correspondant à la condition 
        """
        self._controleur = controleur
        self._ia1 = ia1
        self._ia2 = ia2
        self._condition = condition

    def start(self):
        #Initialisation des 2 sous IA
        self._ia1.start()
        self._ia2.start()
        pass

    def stop(self):
        #Arrêt si l'une des deux IA est finie
        return self._ia1.stop() or self._ia2.stop()

    def step(self):
        if self._controleur.evaluerCondition(self._condition):
            self._ia1.step()
        else:
            self._ia2.step()




class IAWhile:
    """
    Classe permettant de réaliser une ia tant qu'une condition est vérifiée
    """
    def __init__(self, controleur, ia, condition):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia: ia à appeler tant que la condition est vérifiée
        :param condition: IACondition correspondant à la condition du while
        """
        self._controleur = controleur
        self._ia = ia
        self._condition = condition

    def start(self):
        #Initialisation de la sous IA
        self._ia.start()
        pass

    def stop(self):
        #Arrêt si la condition n'est pas vérifiée
        return not self._controleur.evaluerCondition(self._condition)
        
    def step(self):
        #Reset de l'IA
        if self._ia.stop():
            self._ia.start()

        #Step
        self._ia.step()
    


class IAFor:
    """
    Classe permettant de réaliser une ia un certain nombre de fois
    """
    def __init__(self, controleur, ia, nbIter):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia: ia à appeler si la condition est vérifiée
        :param nbIter: nombre de fois que l'ia doit être effectuée
        """
        self._controleur = controleur
        self.v = 0
        self._ia = ia
        self._nbIter = nbIter

    def start(self):
        #Initialisation de i
        self._i = 0

        #Substitution de la variable
        self._vars = [self._nbIter]
        self._controleur.substituerVariables(self)
        
        self._max = int(self._vars[0])
        self._ia.start()
        pass

    def stop(self):
        #Arrêt si l'une des deux IA est
        if self._ia.stop():
            self._i += 1
            if(self._i >= self._max):
                return True
            else:
                self._ia.end()
                self._ia.start()

    def step(self):
        self._ia.step()


class IASeq:
    """
    Classe permettant de réaliser une séquence d'IA
    """
    def __init__(self, controleur, iaList):
        """
        Paramètres
        :param controleur: controleur du robot
        :param iaList: liste des ia à effectuer
        """
        self._controleur = controleur
        self.v = 0
        self._i = -1
        self._iaList = iaList.copy()

    def start(self):
        #Initialisation de la sous ia 1
        self._i = 0

        self._iaList[self._i].start()

    def stop(self):
        #Passage à l'ia suivante si fini
        if self._iaList[self._i].stop():
            if(self._i >= len(self._iaList) - 1):
                return True

    def step(self):
        if self._iaList[self._i].stop():
            self._i += 1
            self._iaList[self._i].start()
        else:
            self._iaList[self._i].step()


class IAFonction():
    def __init__(self, controleur, args):
        self._controleur = controleur
        self.args = args

    def start(self):
        fun = self.args[0]
        args = self.args[1:]
        eval("self._controleur." + fun + "(args)")
        
    def stop(self):
        return True