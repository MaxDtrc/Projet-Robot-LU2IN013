import pygame
import random
from math import radians, cos, sin

import objets as o
import simulation as s


COULEUR_OBSTACLES = (65, 0, 55)
COULEUR_ROBOT = (255, 165, 165)

class Affichage :
    def __init__(self, simulation : s.Simulation, echelle: int = 1):
        """
        Constructeur de la classe affichae
        
        Paramètres:
        simulation -> Simulation concernée par cet affichage
        """
        pygame.init()
        self._echelle = echelle
        self._screen = pygame.display.set_mode((simulation.getTerrain().getSizeX() * self._echelle, simulation.getTerrain().getSizeY() * self._echelle))
        pygame.display.set_caption('Test de la simulation du robot') 
        self._screen.fill((255,255,255))

    def _afficherObstacle(self, obstacle : o.Obstacle):
        """
        Affiche un obstacle sur la fenêtre
        
        Paramètres:
        obstacle -> Obstacle à afficher
        """
        e = self._echelle
        if (isinstance(obstacle, o.ObstacleRectangle)):
            pygame.draw.rect(self._screen, COULEUR_OBSTACLES, (obstacle.getX()*e + self._screen.get_size()[0]/2 - obstacle.getLongueur()*e/2, obstacle.getY()*e + self._screen.get_size()[1]/2 - obstacle.getLargeur()*e/2, obstacle.getLongueur()*e, obstacle.getLargeur()*e))
        elif (isinstance(obstacle, o.ObstacleRond)):
            pygame.draw.circle(self._screen, COULEUR_OBSTACLES, (obstacle.getX()*e + self._screen.get_size()[0]/2, obstacle.getY()*e + self._screen.get_size()[0]/2), obstacle.getRayon()*e)

    def _afficherRobot(self, robot: o.Robot):
        """
        Affiche un robot sur la fenêtre
        
        Paramètres:
        robot -> Robot à afficher
        """
        e = self._echelle
        #Image de base
        image_pas_tournee = pygame.image.load("robot.png").convert_alpha()
        image_pas_tournee = pygame.transform.scale(image_pas_tournee, (image_pas_tournee.get_width()*e, image_pas_tournee.get_height()*e))
        
        #Image que l'on tourne en fonction de l'angle du robot
        image = pygame.transform.rotate(image_pas_tournee, robot.getAngle())

        #Affichage du robot sur le self._screen
        pygame.draw.circle(self._screen, COULEUR_ROBOT, (robot.getX()*e + self._screen.get_size()[0]/2, robot.getY()*e + self._screen.get_size()[0]/2), robot.getRayon()*e)
        self._screen.blit(image, (self._screen.get_size()[0]/2 - image.get_width()/2 + robot.getX()*e, self._screen.get_size()[1]/2 - image.get_height()/2 + robot.getY()*e))


    def afficherSimulation(self, simulation : s.Simulation):
        """
        Affiche l'ensemble de la simulation sur la fenêtre
        
        Paramètres:
        simulation: simulation à afficher
        """
        e = self._echelle
        #Fill de l'écran
        self._screen.fill((255,255,255))

        #Affichage des objets
        for i in range(0, simulation.getNombreDeRobots()):
            r = simulation.getRobot(i)
            t = simulation.getTerrain()
            self._afficherRobot(r)

            #Affichage du capteur de distance
            pygame.draw.line(self._screen, (255, 0, 0), ((r.getX() + cos(radians(r.getAngle())) * r.getRayon())*e + t.getSizeX()*e/2, (r.getY() + sin(radians(-r.getAngle())) * r.getRayon())*e + t.getSizeY()*e/2), (simulation.lastPosX*e  + t.getSizeX()*e/2, simulation.lastPosY*e  + t.getSizeY()*e/2))
        for i in range(0, t.getNombreObstacles()):
            self._afficherObstacle(t.getObstacle(i))

        #Actualisation de l'écran
        pygame.display.update()     
