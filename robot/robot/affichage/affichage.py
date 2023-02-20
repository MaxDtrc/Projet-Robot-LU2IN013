import pygame
from math import radians, cos, sin, degrees
import os
from threading import Thread
import time

from .. import simulation as s


COULEUR_OBSTACLES = (65, 0, 55)
COULEUR_ROBOT = (255, 165, 165)
BLACK = (0, 0, 0)

class Affichage(Thread):
    def __init__(self, simulation : s.Simulation, controleur, fps: int, echelle: int = 1, afficherDistance: bool = False, afficherTrace: bool = False):
        """
        Constructeur de la classe affichage
        
        :param simulation : Simulation concernée par cet affichage
        """
        super(Affichage, self).__init__()
        self._simulation = simulation
        self._controleur = controleur
        self._fps = fps
        self._echelle = echelle
        self._afficherDistance = afficherDistance
        self._afficherTrace = afficherTrace
        self.tailleTrace = 2

        #Init de pygame
        pygame.init()
        self._trace = pygame.surface.Surface((simulation.terrain.sizeX * self._echelle, simulation.terrain.sizeY * self._echelle))
        self._screen = pygame.display.set_mode((simulation.terrain.sizeX * self._echelle, simulation.terrain.sizeY * self._echelle))
        pygame.display.set_caption('Test de la simulation du robot') 
        self._screen.fill((255,255,255))
        self._trace.fill((255, 255, 255))
        

    def run(self):
        self.running = True
        while self.running:
            self.afficherSimulation()
            time.sleep(1./self._fps)

    def stop(self):
        self.running = False

    def _afficherObstacle(self, obstacle : s.Obstacle):
        """
        Affiche un obstacle sur la fenêtre
        
        :param obstacle : Obstacle à afficher
        """
        e = self._echelle
        if (obstacle.type == 0):
            #Affichage d'un obstacle rectangle
            pygame.draw.rect(self._screen, COULEUR_OBSTACLES, (obstacle.x*e + self._screen.get_size()[0]/2 - obstacle.longueur*e/2, obstacle.y*e + self._screen.get_size()[1]/2 - obstacle.largeur*e/2, obstacle.longueur*e, obstacle.largeur*e))
        elif (obstacle.type == 1):
            #Affichage d'un obstacle rond
            pygame.draw.circle(self._trace, COULEUR_OBSTACLES, (obstacle.x*e + self._screen.get_size()[0]/2, obstacle.y*e + self._screen.get_size()[0]/2), obstacle.rayon*e)

    def _afficherRobot(self, robot: s.Robot):
        """
        Affiche un robot sur la fenêtre
        
        :param robot : Robot à afficher
        """
        e = self._echelle
        #Image de base
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        image_pas_tournee = pygame.image.load("robot.png").convert_alpha()
        image_pas_tournee = pygame.transform.scale(image_pas_tournee, (image_pas_tournee.get_width()/15 * robot.rayon *e, image_pas_tournee.get_height()/15 * robot.rayon *e))
        
        #Image que l'on tourne en fonction de l'angle du robot
        image = pygame.transform.rotate(image_pas_tournee, degrees(robot.angle))

        #Affichage du robot sur le self._screen
        pygame.draw.circle(self._screen, COULEUR_ROBOT, (robot.x*e + self._screen.get_size()[0]/2, robot.y*e + self._screen.get_size()[0]/2), robot.rayon*e)
        self._screen.blit(image, (self._screen.get_size()[0]/2 - image.get_width()/2 + robot.x*e, self._screen.get_size()[1]/2 - image.get_height()/2 + robot.y*e))

        if self._afficherTrace:
            #affichage du tracé du robot sur la surface
            pygame.draw.circle(self._trace, BLACK, (robot.x*e + self._trace.get_size()[0]/2, robot.y*e + self._trace.get_size()[0]/2), self.tailleTrace)


    def afficherSimulation(self):
        """
        Affiche l'ensemble de la simulation sur la fenêtre
        
        :param simulation : simulation à afficher
        """
        e = self._echelle

        #Fill de l'écran
        #self._screen.fill((255,255,255))

        #Affichage du tracé
        self._screen.blit(self._trace, (0, 0))
        
        #Affichage des objets
        t = self._simulation.terrain
        for i in range(0, self._simulation.getNombreDeRobots()):
            r = self._simulation.getRobot(i)
            self._afficherRobot(r)

            #Affichage du capteur de distance
            if self._afficherDistance and self._simulation.capteurDistanceAppele:
                pygame.draw.line(self._screen, (255, 0, 0), ((r.x + cos(r.angle) * r.rayon)*e + t.sizeX*e/2, (r.y + sin(-r.angle) * r.rayon)*e + t.sizeY*e/2), (self._simulation.lastPosX*e  + t.sizeX*e/2, self._simulation.lastPosY*e  + t.sizeY*e/2))
                self._simulation.capteurDistanceAppele = False
        for i in range(0, t.getNombreObstacles()):
            self._afficherObstacle(t.getObstacle(i))

        #Actualisation de l'écran
        pygame.display.update()
        
        #Fermeture de la fenêtre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                self._simulation.stop() #On arrête la simulation
                self._controleur.stop_ia_thread() #On arrête l'ia
                self.stop() #On arrête l'affichage
                exit() #On arrête.
