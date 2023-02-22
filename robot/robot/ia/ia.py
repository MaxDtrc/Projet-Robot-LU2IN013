from threading import Thread
import time
from math import pi, radians, degrees


TAILLE_ROUES = 7
RAYON_ROBOT = 5

"""def chargerIA(fichier: str, controleur):
    Création d'une séquence d'IA depuis un fichier
    
    :param fichier: nom du fichier
    :param controleur: controleur pour l'IA
    loop = False
    lst = []
    with open(fichier, 'r') as f:
        l = f.readline()
        while l:
            t = l.split(" ")
            match t[0]:
                case "avancer":
                    lst.append(Avancer(controleur, int(t[1]), int(t[2])))
                case "tourner_droite":
                    lst.append(TournerDroite(controleur, int(t[1]), int(t[2])))
                case "approcher_mur":
                    lst.append(ApprocherMur(controleur, int(t[1])))
                case "boucler":
                    loop = True
            l = f.readline()
    return (lst, loop)"""


class IA(Thread):
    """
    Classe représentant l'IA
    """
    def __init__(self, controleur, strat, dT = 0.01):
        super(IA, self).__init__()
        self._controleur = controleur
        self.strategies = strat[0]
        self.boucler = strat[1]
        self.currentStrat = -1
        self._wait = dT

    def run(self):
        if len(self.strategies) != 0:
            self._controleur.running = True
            while self._controleur.running:
                #Etape suivante
                self._lastTime = time.time()
                time.sleep(self._wait)
                self._dT = time.time() - self._lastTime
                self.step()


        
    def step(self):
        if self.currentStrat == -1 or self.strategies[self.currentStrat].stop():
            #On arrête la stratégie "proprement" et on passe à la stratégie suivante
            if self.currentStrat != -1: 
                self.strategies[self.currentStrat].end()
            self.currentStrat += 1
            if self.currentStrat >= len(self.strategies):
                if self.boucler:
                    #On repasse à la première stratégie
                    self.currentStrat = 0
                else:
                    self.currentStrat = 0
                    self._controleur.running = False
                    return
            #Initialisation de la stratégie
            self._controleur.reset()
            self.strategies[self.currentStrat].start()
        else:
            #Step de la stratégie
            self.strategies[self.currentStrat].step(self._dT)        


#IA Basiques
class ReculerDroit:
    """
    Classe représentant l'ia permettant d'avancer droit
    """
    def __init__(self, controleur, distance, v):
        self._controleur = controleur
        self.distance = distance
        self.v = v
        self.parcouru = 0

    def start(self):
        self._controleur.getDistanceParcourue() #Reinitialisation
        self.parcouru = 0

    def stop(self):
        #On avance tant qu'on n'est pas trop près d'un mur/qu'on n' a pas suffisement avancé
        print(self.parcouru)
        self._controleur.getDistance()
        return -self.parcouru > self.distance

    def step(self, dT: float):
        #Calcul de la distance parcourue
        self.parcouru += self._controleur.getDistanceParcourue()

        if self.stop(): 
            self.end()
            return

        self.avancer()

    def end(self):
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

    def avancer(self):
        #Avancer droit: on met la même vitesse à gauche et à droite
        self._controleur.setVitesseGauche(-self.v)
        self._controleur.setVitesseDroite(-self.v)

class Avancer:
    """
    Classe représentant l'ia permettant d'avancer droit
    """
    def __init__(self, controleur, distance, v, angle = 0):
        self._controleur = controleur
        self.distance = distance
        self.angle = angle
        self.v = v
        self.parcouru = 0

    def start(self):
        self._controleur.getDistanceParcourue() #Reinitialisation
        self.parcouru = 0

    def stop(self):
        #On avance tant qu'on n'est pas trop près d'un mur/qu'on n' a pas suffisement avancé
        return self.parcouru > self.distance

    def step(self, dT: float):
        #Calcul de la distance parcourue
        self.parcouru += abs(self._controleur.getDistanceParcourue())

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
            self._controleur.setVitesseGauche(self.v * (1 + self.angle/100))
            self._controleur.setVitesseDroite(self.v)
        else:
            self._controleur.setVitesseGauche(self.v)
            self._controleur.setVitesseDroite(self.v * (1 - self.angle/100))

class TournerSurPlace:
    """
    Classe représentant l'ia permettant de tourner à droite
    """
    def __init__(self, controleur, angle, v):
        self._controleur = controleur
        self.angle = radians(angle)
        if angle >= 0:
            self.v = v
        else:
            self.v = -v
        self.parcouru = 0

    def start(self):
        self.parcouru = 0
        self._controleur.getDecalageAngle()

    def stop(self):
        #On tourne tant qu'on n'a pas dépassé l'angle
        return self.parcouru > abs(self.angle) 
        
    def step(self, dT : float):
        #Calcul de la distance parcourue
        self.parcouru += abs(self._controleur.getDecalageAngle())

        if self.stop():
            self.end()
            return

        self.avancer()

    def end(self):
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

    def avancer(self):
        self._controleur.setVitesseGauche(self.v)
        self._controleur.setVitesseDroite(-self.v)

class ApprocherMur:
    """
    Classe représentant l'ia permettant d'approcher un mur jusqu'à une certaine distance
    """
    def __init__(self, controleur, distance):
        self._controleur = controleur
        self.v = 0
        self.d = distance

    def start(self):
        #Aucune initialisation
        pass

    def stop(self):
        #Avance vers le mur jusqu'à être à la distance donnée
        return self._controleur.getDistance() < self.d

    def step(self, dT: float):
        #Calcul de la distance au mur
        distance = self._controleur.getDistance()

        if self.stop(): 
            self.end()
            return
        else:
            #Calcul de la vitesse en conséquence
            self.v = distance * 2
            self.avancer()
    
    def end(self):
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

    def avancer(self):
        #Avancer droit: on met la même vitesse à gauche et à droite
        self._controleur.setVitesseGauche(self.v)
        self._controleur.setVitesseDroite(self.v)

#IA complexes
class IACondition:
    """
    Classe permettant de réaliser une ia conditionnelle
    """
    def __init__(self, controleur, ia1, ia2, condition):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia1: ia à appeler si la condition est vérifiée
        :param ia2: ia à appeler si la condition n'est pas vérifiée
        :param condition: fonction de la condition qui renvoie un booléen
        """
        self._controleur = controleur
        self.v = 0
        self._ia1 = ia1
        self._ia2 = ia2
        self._condition = condition

    def start(self):
        #Initialisation des 2 sous IA
        self._ia1.start()
        self._ia2.start()
        pass

    def stop(self):
        #Arrêt si l'une des deux IA est
        return self._ia1.stop() or self._ia2.stop()

    def step(self, dT: float):
        if self.stop(): 
            self.end()
            return
        else:
            if self._condition(self._controleur):
                self._ia1.step(dT)
            else:
                self._ia2.step(dT)
    
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
        :param ia: ia à appeler si la condition est vérifiée
        :param condition: fonction de la condition qui renvoie un booléen
        """
        self._controleur = controleur
        self.v = 0
        self._ia = ia
        self._condition = condition

    def start(self):
        #Initialisation des 2 sous IA
        self._ia.start()
        pass

    def stop(self):
        #Arrêt si l'une des deux IA est
        return self._ia.stop() or not self._condition(self._controleur)

    def step(self, dT: float):
        if self.stop(): 
            self.end()
            return
        else:
            if self._condition(self._controleur):
                self._ia.step(dT)
    
    def end(self):
        self._ia.end()