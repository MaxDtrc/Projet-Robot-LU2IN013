from threading import Thread
import time
from math import pi, radians, degrees


TAILLE_ROUES = 7
RAYON_ROBOT = 5


class IA(Thread):
    def __init__(self, controleur, dT = 0.01):
        super(IA, self).__init__()
        self._controleur = controleur
        #Liste des stratégies à réaliser (pour l'instant en boucle)
        #self.strategies = [AvancerDroit(controleur, 20, 720), TournerDroite(controleur, 90, 90)]
        self.strategies = [ApprocherMur(controleur)] 
        self.boucler = False
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
            #On passe à la stratégie suivante
            print("Changement de stratégie")
            #On arrête la stratégie "proprement"
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
    def __init__(self, controleur):
        self._controleur = controleur
        self.v = 0

    def start(self):
        #Aucune initialisation
        pass

    def stop(self):
        #Avance jusqu'à être le plus prêt possible du mur
        return self._controleur.getDistance() < 2

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