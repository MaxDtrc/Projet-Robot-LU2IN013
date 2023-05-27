from threading import Thread
import time
from math import pi, radians, degrees
from random import randint



class IA(Thread):
    """
    Classe représentant l'IA
    """
    def __init__(self, controleur, strat, dT):
        """
        Constructeur de la classe IA
        :param controleur: le controleur
        :param strat: la stratagie choisie (ia à executer)
        :param dT: le dT de l actualisation de la simulation
        """
        super(IA, self).__init__()
        self._controleur = controleur
        self.strategie = strat
        self._wait = dT

    def run(self):
        """
        Lancement du thread de l IA
        """
        self.strategie.start()
        self._controleur.running = True
        while self._controleur.running:
            #Etape suivante
            self._lastTime = time.time()
            time.sleep(self._wait)
            self._dT = time.time() - self._lastTime
            self.step()

    def step(self):
        """
        Arret de l IA si fin de stratégie
        """
        if not self.strategie.stop():
            self.strategie.step()
        else:
            self._controleur.stop()
            self._controleur.running = False





#IA de déplacement
class Avancer:
    """
    Classe représentant l'ia permettant d'avancer droit
    """
    def __init__(self, c, d, v, a=0):
        """
        Constructeur de la classe Avancer
        :param c: controleur du robot
        :param d: distance (cm) dont le robot doit avancer
        :param v: vitesse (tour de roue/s)
        :param a: angle de la trajectoire du robot (pourcentage de -100 à 100)
        """
        self._controleur = c
        self.d, self.a, self.v, self.parcouru = d, a, v, 0

    def start(self):
        """
        Permet de lancer le thread de l IA
        """
        #On reset le controleur
        self._controleur.resetDecalage()

        #Substitution des variables
        self._vars = [self.d, self.a, self.v]
        self._controleur.substituerVariables(self._vars)
        self.distance, self.angle, self.vitesse = [float(i) for i in self._vars]

        #Initialisation de la distance
        self.posInitiale = self._controleur.getDistanceParcourue()
        self.parcouru = 0


    def stop(self):
        """
        Permet de stopper le thread de l IA
        """
        #On avance tant qu'on n' a pas suffisement avancé
        return self.parcouru >= abs(self.distance)

    def step(self):
        """
        Permet de stopper le thread de l IA une fois la distance parcourue
        """
        #Calcul de la distance parcourue
        self.parcouru = abs(self._controleur.getDistanceParcourue() - self.posInitiale)

        self._controleur.setVitesseGauche(self.vitesse * (1 + self.angle/100) if self.angle <= 0 else self.vitesse)
        self._controleur.setVitesseDroite(self.vitesse if self.angle <= 0 else self.vitesse * (1 - self.angle/100))


class TournerSurPlace:
    """
    Classe représentant l'IA permettant de tourner à droite    
    """

    def __init__(self, c, a, v):
        """
        Constructeur de la classe TournerSurPlace
        :param controleur: controleur du robot
        :param angle: angle (degré) de rotation
        :param v: vitesse (tour de roue/s)
        """
        self._controleur = c
        self.a = a
        self.v = v
        self.parcouru = 0

    def start(self):
        """
        Permet de lancer le thread de l IA
        """
        #On reset le controleur
        self._controleur.resetDecalage()

        #Substitution des variables
        self._vars = [self.a, self.v]
        self._controleur.substituerVariables(self._vars)
        self.angle = radians(float(self._vars[0]))
        self.vitesse = float(self._vars[1]) if self.angle >= 0 else -float(self._vars[1])        

        #Initialisation de la distance
        self.posInitiale = self._controleur.getDecalageAngle()
        self.parcouru = 0
        

    def stop(self):
        """
        Permet de stoper le thread de l IA
        """
        #On tourne tant qu'on n'a pas dépassé l'angle
        return self.parcouru >= abs(self.angle)
        
    def step(self):
        """
        Execution du thread de l IA tant que la distance à parcourir n a pas été effectué
        """
        #Calcul de la distance parcourue
        self.parcouru = abs(self._controleur.getDecalageAngle() - self.posInitiale) 

        self._controleur.setVitesseGauche(self.vitesse)
        self._controleur.setVitesseDroite(-self.vitesse)

class TournerTete:
    """
    Classe représentant l'ia permettant de tourner la tete du robot
    """
    def __init__(self, c, a):
        """
        Constructeur de la classe TournerTete
        :param angle: angle (degré) de rotation
        :param c: controleur
        """
        self._controleur = c
        self.a = a

    def start(self):
        """
        Lancement du thread de l IA
        """
        #Substitution des variables
        self._vars = [self.a]
        self._controleur.substituerVariables(self._vars)
        self.angle = 180 - float(self._vars[0])
        self._controleur.setCerveau(self.angle)

    def stop(self):
        """
        Arret du thread de l IA
        """
        return True

class Stop:
    """
    Classe représentant l'ia permettant au robot de s'arrêter
    """
    def __init__(self, c):
        """
        Constructeur de la classe Stop
        :param c: controleur du robot
        """
        self._controleur = controleur

    def start(self):
        """
        Lancement du thread de l IA
        """
        #On met les vitesses à 0
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

    def stop(self):
        """
        Arret du thread de l IA
        """
        #On s'arrête directement
        return True


#IA complexes
class IAIf:
    """
    Classe permettant de réaliser un "if"
    """
    def __init__(self, c, ia1, ia2, condition):
        """
        Constructeur de la classe IAIf
        Paramètres
        :param c: controleur du robot
        :param ia1: ia à appeler si la condition est vérifiée
        :param ia2: ia à appeler si la condition n'est pas vérifiée
        :param condition: IACondition correspondant à la condition du if
        """
        self._controleur = c
        self._ia1 = ia1
        self._ia2 = ia2
        self._condition = condition

    def start(self):
        """
        Lancement du thread de l IA
        """
        #Initialisation des 2 sous IA
        if self._controleur.evaluerCondition(self._condition):
            self._ia = self._ia1
        else:
            self._ia = self._ia2

        if(self._ia != None):
            self._ia.start()


    def stop(self):
        """
        Arret du thread de l IA
        """
        #Arrêt si l'une des deux IA est finie
        return self._ia == None or self._ia.stop()

    def step(self):
        """
        Execution du thread de l IA tant que la condition est vraie
        """
        if(self._ia != None):
            self._ia.step()
    

#IA complexes
class IAAlterner:
    """
    Classe permettant de réaliser une ia conditionnelle (réalise un step d'une des deux IA selon la condition)
    """
    def __init__(self, c, ia1, ia2, condition):
        """
        Constructeur de la classe IAAlterner
        Paramètres
        :param c: controleur du robot
        :param ia1: ia à appeler si la condition est vérifiée
        :param ia2: ia à appeler si la condition n'est pas vérifiée
        :param condition: IACondition correspondant à la condition 
        """
        self._controleur = c
        self._ia1 = ia1
        self._ia2 = ia2
        self._condition = condition

    def start(self):
        """
        Lancement du thread de l IA
        """
        #Initialisation des 2 sous IA
        self._ia1.start()
        self._ia2.start()
        pass

    def stop(self):
        """
        Arret du thread de l IA
        """
        #Arrêt si l'une des deux IA est finie
        return self._ia1.stop() or self._ia2.stop()

    def step(self):
        """
        Execution de l IA pas à pas
        """
        if self._controleur.evaluerCondition(self._condition):
            self._ia1.step()
        else:
            self._ia2.step()




class IAWhile:
    """
    Classe permettant de réaliser une ia tant qu'une condition est vérifiée
    """
    def __init__(self, c, ia, condition):
        """
        Constructeur de la classe IAWhile
        Paramètres
        :param c: controleur du robot
        :param ia: ia à appeler tant que la condition est vérifiée
        :param condition: IACondition correspondant à la condition du while
        """
        self._controleur = c
        self._ia = ia
        self._condition = condition

    def start(self):
        """
        Lancement du thread de l IA
        """
        #Initialisation de la sous IA
        self._ia.start()
        pass

    def stop(self):
        """
        Arret du thread de l IA
        """
        #Arrêt si la condition n'est pas vérifiée
        return not self._controleur.evaluerCondition(self._condition)
        
    def step(self):
        """
        Execution du thread de l IA tant que la condition du while est vraie
        """
        #Reset de l'IA
        if self._ia.stop():
            self._ia.start()

        #Step
        if not self._ia.stop():
            self._ia.step()
    


class IAFor:
    """
    Classe permettant de réaliser une ia un certain nombre de fois
    """
    def __init__(self, c, ia, nbIter):
        """
        Constructeur de la classe IAFor
        Paramètres
        :param c: controleur du robot
        :param ia: ia à appeler si la condition est vérifiée
        :param nbIter: nombre de fois que l'ia doit être effectuée
        """
        self._controleur = c
        self.v = 0
        self._ia = ia
        self._nbIter = nbIter

    def start(self):
        """
        Lancement du thread de l IA
        """
        #Initialisation de i
        self._i = 0

        #Substitution de la variable
        self._vars = [self._nbIter]
        self._controleur.substituerVariables(self._vars)
        
        self._max = int(self._vars[0])
        self._ia.start()
        pass

    def stop(self):
        """
        Arret du thread de l IA
        """
        #Arrêt si l'une des deux IA est
        if self._ia.stop():
            self._i += 1
            if(self._i >= self._max):
                return True
            else:
                self._ia.start()

    def step(self):
        """
        Execution du thread de l IA tant que la boucle for n est pas finie
        """
        if not self._ia.stop():
            self._ia.step()


class IASeq:
    """
    Classe permettant de réaliser une séquence d'IA
    """
    def __init__(self, c, iaList):
        """
        Constructeur de la classe IASeq
        Paramètres
        :param c: controleur du robot
        :param iaList: liste des ia à effectuer
        """
        self._controleur = c
        self.v = 0
        self._i = -1
        self._iaList = iaList.copy()

    def start(self):
        """
        Lancement du thread de l IA
        """
        #Initialisation de la sous ia 1
        self._i = 0

        self._iaList[self._i].start()

    def stop(self):
        """
        Arret du thread de l IA
        """
        #Passage à l'ia suivante si fini
        if self._iaList[self._i].stop():
            if(self._i >= len(self._iaList) - 1):
                return True

    def step(self):
        """
        Execution de l IA tant que la sequence n est pas finie
        """
        if self._iaList[self._i].stop():
            self._controleur.stop()
            self._i += 1
            self._iaList[self._i].start()
        else:
            self._iaList[self._i].step()


class IAFonction():
    """
    Classe permettant de réaliser une ia avec une certaine fonction
    """
    def __init__(self, c, args):
        """
        Constructeur de la classe IAFonction
        :param c: le controleur
        :param args: les arguments de la fonction
        """
        self._controleur = c
        self.args = args

    def start(self):
        """
        Lancement du thread de l IA
        """
        fun = self.args[0]
        args = self.args[1:]
        eval("self._controleur." + fun + "(args)")
    
    def stop(self):
        """
        Arret du thread de l IA
        """
        return True
