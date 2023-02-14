from threading import Thread
import time
from math import pi, radians, degrees


TAILLE_ROUES = 7
RAYON_ROBOT = 5



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
            self.running = True
            while self.running:
                #Etape suivante
                self._lastTime = time.time()
                time.sleep(self._wait)
                self._dT = time.time() - self._lastTime
                self.step()
        
    def step(self):
        if self.strategies[self.currentStrat].stop() or self.currentStrat == -1:
            #On arrête la stratégie "proprement" et on passe à la stratégie suivante
            if self.currentStrat != -1: self.strategies[self.currentStrat].end()
            self.currentStrat += 1
            if self.currentStrat >= len(self.strategies):
                if self.boucler:
                    #On repasse à la première stratégie
                    self.currentStrat = 0
                else:
                    self.running = False
                    return
            #Initialisation de la stratégie
            self.strategies[self.currentStrat].start()

        #Step de la stratégie
        self.strategies[self.currentStrat].step(self._dT)
    

class AvancerDroit:
    """
    Classe représentant l'ia permettant d'avancer droit
    """
    def __init__(self, controleur, distance, v):
        self._controleur = controleur
        self.distance = distance
        self.v = v
        self.parcouru = 0

    def start(self):
        self.parcouru = 0

    def stop(self):
        #On avance tant qu'on n'est pas trop près d'un mur/qu'on n' a pas suffisement avancé
        return self.parcouru > self.distance or self._controleur.getDistance() < 10 

    def step(self, dT: float):
        #Calcul de la distance parcourue
        self.parcouru += self.v/360 * pi * TAILLE_ROUES * dT

        if self.stop(): 
            self.end()
            return

        self.avancer()

    def end(self):
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

    def avancer(self):
        #Avancer droit: on met la même vitesse à gauche et à droite
        self._controleur.setVitesseGauche(self.v)
        self._controleur.setVitesseDroite(self.v)

class TournerDroite:
    """
    Classe représentant l'ia permettant de tourner à droite
    """
    def __init__(self, controleur, angle, v):
        self._controleur = controleur
        self.angle = radians(-angle)
        self.v = v
        self.parcouru = 0

    def start(self):
        self.parcouru = 0

    def stop(self):
        #On tourne tant qu'on n'a pas dépassé l'angle
        return self.parcouru < self.angle 
        
    def step(self, dT: float):
        #Calcul des vitesses gauches et droites en distance
        vG = self.v/360.0 * pi * TAILLE_ROUES
        vD = -vG

        #Calcul de la distance parcourue
        self.parcouru += (vD - vG)/(RAYON_ROBOT * 2) * dT

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