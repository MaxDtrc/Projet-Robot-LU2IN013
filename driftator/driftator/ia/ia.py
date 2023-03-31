from threading import Thread
import time
from math import pi, radians, degrees
from random import randint


TAILLE_ROUES = 7
RAYON_ROBOT = 5




class IA(Thread):
    """
    Classe représentant l'IA
    """
    def __init__(self, controleur, strat, dT):
        super(IA, self).__init__()
        self._controleur = controleur
        self.strategie = strat
        self._wait = dT/10

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
            self.strategie.step(self._dT)
        else:
            self.strategie.end()
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
        self.lastStep = 0

    def start(self):
        self._controleur.getDistanceParcourue(self) #Reinitialisation
        self.parcouru = 0

        #Substitution des variables
        self._vars = [self.d, self.a, self.v]
        for i in range(3):
            substituerVariables(self, i)
        self.distance = float(self._vars[0])
        self.angle = float(self._vars[1])
        self.vitesse = float(self._vars[2])

        self.avancer()
        
        

    def stop(self):
        #On avance tant qu'on n'est pas trop près d'un mur/qu'on n' a pas suffisement avancé
        return self.parcouru >= self.distance

    def step(self, dT: float):
        #Calcul de la distance parcourue
        d = abs(self.lastStep)
        self.parcouru += abs(self._controleur.getDistanceParcourue(self)) - d

        if self.stop(): 
            self.end()
            return
        
        self.avancer()

        

    def end(self):
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

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
        self.lastStep = 0
        self.parcouru = 0


    def start(self):
        self._controleur.getDecalageAngle(self)
        self.parcouru = 0

        #Substitution des variables
        self._vars = [self.a, self.v]
        for i in range(2):
            substituerVariables(self, i)
            
        self.angle = radians(float(self._vars[0]))
        if self.angle >= 0:
            self.vitesse = float(self._vars[1])
        else:
            self.vitesse = -float(self._vars[1])

        self.avancer()

    def stop(self):
        #On tourne tant qu'on n'a pas dépassé l'angle
        return self.parcouru > abs(self.angle)
        
    def step(self, dT : float):
        #Calcul de la distance parcourue
        d = abs(self.lastStep)
        a = abs(self._controleur.getDecalageAngle(self))
        if(a != 0):
            self.parcouru += a - d

        if self.stop():
            self.end()
            return

        self.avancer()

    def end(self):
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

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
        self._condition.start()
        self._condition.step()
        if(self._condition.resultat):
            self._ia = self._ia1
        else:
            self._ia = self._ia2
        self._ia.start()


    def stop(self):
        #Arrêt si l'une des deux IA est finie
        return self._ia.stop()

    def step(self, dT: float):
        if self.stop(): 
                self.end()
                return
        else:
            self._ia.step(dT)
    
    def end(self):
        self._ia.stop()

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
        self._condition.start()
        self._ia1.start()
        self._ia2.start()
        pass

    def stop(self):
        #Arrêt si l'une des deux IA est finie
        return self._ia1.stop() or self._ia2.stop()

    def step(self, dT: float):
        if not self._condition.stop():
            self._condition.step()
        else:
            if self.stop(): 
                self.end()
                return
            else:
                if self._condition.resultat:
                    self._ia1.step(dT)
                else:
                    self._ia2.step(dT)
            self._condition.start()
    
    def end(self):
        self._ia1.end()
        self._ia2.end()



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
        self._condition.start()
        self._ia.start()
        pass

    def stop(self):
        #Arrêt si la condition n'est pas vérifiée
        if not self._condition.stop():
            self._condition.step()
        if not self._condition.resultat:
            return True
        self._condition.start()

    def step(self, dT: float):
        if self.stop(): 
            self.end()
            return
        else:
            #Reset de l'IA
            if self._ia.stop():
                self._ia.end()
                self._ia.start()

            #Step
            self._ia.step(dT)
    
    def end(self):
        self._ia.end()

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
        substituerVariables(self, 0)
        
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

    def step(self, dT: float):
        if self.stop(): 
            self.end()
            return
        else:
            self._ia.step(dT)
    
    def end(self):
        self._ia.end()

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
                

    def step(self, dT: float):
        if self.stop(): 
            self.end()
            return
        elif self._iaList[self._i].stop():
            self._iaList[self._i].end()
            self._i += 1
            self._iaList[self._i].start()
            
        self._iaList[self._i].step(dT)
    
    def end(self):
        self._iaList[self._i].end()














#IA complémentaires


def substituerVariables(ia, i):
    """
    Fonctions auxiliaire permettant de remplacer les variables par leur valeurs
    """
    try:
        #L'élément est une valeur
        parsed = float(ia._vars[i])
    except:
        #L'élément est un nom de variable

        #Variables custom
        if(ia._vars[i] == "capteur_distance"):
            ia._controleur._variables["capteur_distance"] = ia._controleur.getDistance()
        if(ia._vars[i] == "capteur_balise"):
            ia._controleur._variables["capteur_balise"] = ia._controleur.getBalisePosition()
        if(ia._vars[i] == "random"):
            ia._controleur._variables["random"] = randint(0, 10000000)

        #On substitue la variable à sa valeur
        if(ia._vars[i] not in ['(', ')', '==', '!=', '<', '>', '<=', '>=', '+', '-', '/', '*', '%', '//', "and", "or"]):
            ia._vars[i] = str(ia._controleur._variables[ia._vars[i]])




class IACondition:
    """
    Classe permettant de réaliser une condition pour une IA
    """
    def __init__(self, controleur, args):
        """
        Paramètres
        :param controleur: controleur du robot
        :param args: Tableau splité de la condition
        """
        self._controleur = controleur
        self.resultat = None
        self._args = args

    def start(self):
        #Reset du resultat
        self.resultat = None
        self._vars = self._args.copy()

    def stop(self):
        #Arrêt si la condition a été testée
        return self.resultat != None

    def step(self):
        if not self.stop():
            for i in range(len(self._vars)):
                substituerVariables(self, i)

            self.resultat = eval(' '.join(self._vars))

    def end(self):
        pass

class IAGererVariable:
    """
    Classe permettant de modifier une variable
    """
    def __init__(self, controleur, args):
        """
        Paramètres
        :param controleur: controleur du robot
        :param args: Tableau splité de l'instruction
        """
        self._controleur = controleur
        self.effectue = False
        self._args = args

    def start(self):
        #Reset du resultat
        self.effectue = False
        self._vars = self._args.copy()

    def stop(self):
        #Arrêt si l'instruction a été effectuée
        return self.effectue != False

    def step(self, dT):
        if not self.stop():
            for i in range(2, len(self._vars)):
                substituerVariables(self, i)

            self._controleur._variables[self._args[0]] = eval(''.join(self._vars[2:]))
            self.effectue = True

    def end(self):
        pass

class IAPrint:
    """
    Classe permettant d'effectuer un affichage
    """
    def __init__(self, controleur, args):
        """
        Paramètres
        :param controleur: controleur du robot
        :param args: Tableau splité de l'instruction
        """
        self._controleur = controleur
        self.effectue = False
        self._args = args

    def start(self):
        #Reset du resultat
        self.effectue = False
        self._vars = self._args.copy()

    def stop(self):
        #Arrêt si l'instruction a été effectuée
        return self.effectue != False

    def step(self, dT):
        if not self.stop():
            for i in range(len(self._vars)):
                substituerVariables(self, i)

            #Affichage
            print(eval(''.join(self._vars)))
            self.effectue = True

    def end(self):
        pass