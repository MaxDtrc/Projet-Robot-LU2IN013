from threading import Thread
import time
from math import pi, degrees, radians


TAILLE_ROUES = 5
RAYON_ROBOT = 7


class IA(Thread):
    def __init__(self, controleur, dT = 0.01):
        super(IA, self).__init__()
        self._controleur = controleur
        self.strategies = [AvancerDroit(controleur, 100, 720), TournerDroite(controleur, 90, 90)] #Liste des stratégies à réaliser (pour l'instant en boucle)
        self.currentStrat = -1
        self._dT = dT

    def run(self):
        if len(self.strategies) != 0:
            while True:
                self.step()
                time.sleep(self._dT)
        
    def step(self):
        #On passe à la stratégie suivante
        if self.strategies[self.currentStrat].stop() or self.currentStrat == -1:
            print("Changement de stratégie")
            self.currentStrat += 1
            if self.currentStrat >= len(self.strategies):
                self.currentStrat = 0
            self.strategies[self.currentStrat].start()
        
        #Step de la stratégie
        self.strategies[self.currentStrat].step(self._dT)
    

class AvancerDroit:
    def __init__(self, controleur, distance, v):
        self._controleur = controleur
        self.distance = distance
        self.v = v
        self.parcouru = 0

    def start(self):
        self.parcouru = 0

    def stop(self):
        return self.parcouru > self.distance or self._controleur.getDistance() < 20 #On avance tant qu'on n'est pas trop près d'un mur/qu'on n' a pas suffisement avancé
        
    def step(self, dT: float):
        self.parcouru += self.v/360 * pi * TAILLE_ROUES * dT
        if self.stop(): 
            self._controleur.setVitesseGauche(0)
            self._controleur.setVitesseDroite(0)
            return
        self.avancer()


    def avancer(self):
        self._controleur.setVitesseGauche(self.v)
        self._controleur.setVitesseDroite(self.v)

class TournerDroite:
    def __init__(self, controleur, angle, v):
        self._controleur = controleur
        self.angle = angle
        self.v = v
        self.parcouru = 0

    def start(self):
        self.parcouru = 0

    def stop(self):
        return degrees(self.parcouru) < -self.angle #On tourne tant qu'on n'a pas dépassé l'angle
        
    def step(self, dT: float):
        vG = self.v/360.0 * pi * TAILLE_ROUES
        vD = -vG
        
        self.parcouru += (vD - vG)/(RAYON_ROBOT * 2) * dT

        if self.stop():
            self._controleur.setVitesseGauche(0)
            self._controleur.setVitesseDroite(0)
            return
        self.avancer()

    def avancer(self):
        self._controleur.setVitesseGauche(self.v)
        self._controleur.setVitesseDroite(-self.v)