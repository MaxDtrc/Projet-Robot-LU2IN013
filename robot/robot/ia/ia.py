from threading import Thread
import time
from math import pi, radians, degrees


TAILLE_ROUES = 7
RAYON_ROBOT = 5

def chargerIA(fichier: str, controleur):
    """
    Création d'une séquence d'IA depuis un fichier
    
    :param fichier: nom du fichier
    :param controleur: controleur pour l'IA
    """
    loop = False
    lst = []
    with open(fichier, 'r') as f:
        l = f.readline()
        while l:
            t = l.split(" ")
            match t[0]:
                case "avancer":
                    lst.append(AvancerDroit(controleur, int(t[1]), int(t[2])))
                case "tourner_droite":
                    lst.append(TournerDroite(controleur, int(t[1]), int(t[2])))
                case "approcher_mur":
                    lst.append(ApprocherMur(controleur, int(t[1])))
                case "boucler":
                    loop = True
            l = f.readline()
    return (lst, loop)


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
        self._dT = dT

    def run(self):
        if len(self.strategies) != 0:
            self.running = True
            while self.running:
                #Etape suivante
                time.sleep(self._dT)
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
        else:
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
        self._controleur.getDistance()
        return self.parcouru > self.distance

    def step(self, dT: float):
        #Calcul de la distance parcourue
        print(self.parcouru)
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
        self._controleur.getDecalage()

    def stop(self):
        #On tourne tant qu'on n'a pas dépassé l'angle
        return self.parcouru < self.angle 
        
    def step(self, dT : float):
        #Calcul de la distance parcourue
        self.parcouru += self._controleur.getDecalage()

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