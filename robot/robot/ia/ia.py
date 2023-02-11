from threading import Thread
import time
from math import pi, degrees, radians

class IA(Thread):
    def __init__(self, controleur):
        super(IA, self).__init__()
        self._controleur = controleur
        self.strategies = [AvancerDroit(controleur, 100, 720), TournerDroite(controleur, 90, 360)]
        self.currentStrat = -1

    def run(self):
        if len(self.strategies) != 0:
            while True:
                self.step()
                time.sleep(0.1)
        
    def step(self):
        #On passe à la stratégie suivante
        if self.strategies[self.currentStrat].stop() or self.currentStrat == -1:
            print("Changement de stratégie")
            self.currentStrat += 1
            if self.currentStrat >= len(self.strategies):
                self.currentStrat = 0
            self.strategies[self.currentStrat].start()
        
        #Step de la stratégie
        self.strategies[self.currentStrat].step(0.1)
    

class AvancerDroit:
    def __init__(self, controleur, distance, v):
        self._controleur = controleur
        self.distance = distance
        self.v = v
        self.parcouru = 0

    def start(self):
        self.parcouru = 0

    def stop(self):
        return self.parcouru > self.distance or self._controleur.getDistance() < 40
        
    def step(self, dT: float):
        self.parcouru += self.v/360 * pi * 5 * dT
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
        return degrees(self.parcouru) < -self.angle
        
    def step(self, dT: float):
        v = self.v/360.0 * pi * 5
        self.parcouru += (-2.0 * v)/15.0 * dT

        if self.stop(): 
            self._controleur.setVitesseGauche(0)
            self._controleur.setVitesseDroite(0)
            return
        self.avancer()

    def avancer(self):
        self._controleur.setVitesseGauche(self.v)
        self._controleur.setVitesseDroite(-self.v)