import pygame
import random

import objets as o
import simulation as s


COULEUR_OBSTACLES = (65, 0, 55)
COULEUR_ROBOT = (255, 165, 165)

class Affichage :
    def __init__(self, simulation : s.Simulation):
        """
        Constructeur de la classe affichae
        
        Paramètres:
        simulation -> Simulation concernée par cet affichage
        """
        pygame.init()
        self._screen = pygame.display.set_mode((simulation.getTerrain().getSizeX(), simulation.getTerrain().getSizeY()))
        pygame.display.set_caption('Test de la simulation du robot') 
        self._screen.fill((255,255,255))

    def _afficherObstacle(self, obstacle : o.Obstacle):
        """
        Affiche un obstacle sur la fenêtre
        
        Paramètres:
        obstacle -> Obstacle à afficher
        """
        if (isinstance(obstacle, o.ObstacleRectangle)):
            pygame.draw.rect(self._screen, COULEUR_OBSTACLES, (obstacle.getX() + self._screen.get_size()[0]/2 - obstacle.getLongueur()/2,obstacle.getY()+(self._screen.get_size()[1]/2)-obstacle.getLargeur()/2,obstacle.getLongueur(),obstacle.getLargeur()))
        elif (isinstance(obstacle, o.ObstacleRond)):
            pygame.draw.circle(self._screen, COULEUR_OBSTACLES, (obstacle.getX() + self._screen.get_size()[0]/2, obstacle.getY() + self._screen.get_size()[0]/2), obstacle.getRayon())

    def _afficherRobot(self, robot: o.Robot):
        """
        Affiche un robot sur la fenêtre
        
        Paramètres:
        robot -> Robot à afficher
        """
        #Image de base
        image_pas_tournee = pygame.image.load("robot.png").convert_alpha()
        
        #Image que l'on tourne en fonction de l'angle du robot
        image = pygame.transform.rotate(image_pas_tournee, robot.getAngle())

        #Affichage du robot sur le self._screen
        pygame.draw.circle(self._screen, COULEUR_ROBOT, (robot.getX() + self._screen.get_size()[0]/2, robot.getY() + self._screen.get_size()[0]/2), robot.getRayon())
        self._screen.blit(image, (self._screen.get_size()[0]/2 - image.get_width()/2 + robot.getX(), self._screen.get_size()[1]/2 - image.get_height()/2 + robot.getY()))


    def afficherSimulation(self, simulation : s.Simulation):
        """
        Affiche l'ensemble de la simulation sur la fenêtre
        
        Paramètres:
        simulation: simulation à afficher
        """
        #Fill de l'écran
        self._screen.fill((255,255,255))

        #Affichage des objets
        for i in range(0, simulation.getNombreDeRobots()):
            self._afficherRobot(simulation.getRobot(i))
            pygame.draw.line(self._screen, (255, 0, 0), (simulation.getRobot(i).getX() + simulation.getTerrain().getSizeX()/2, simulation.getRobot(i).getY() + simulation.getTerrain().getSizeY()/2), (simulation.lastPosX  + simulation.getTerrain().getSizeX()/2, simulation.lastPosY  + simulation.getTerrain().getSizeY()/2))
        for i in range(0, simulation.getTerrain().getNombreObstacles()):
            self._afficherObstacle(simulation.getTerrain().getObstacle(i))

        #Actualisation de l'écran
        pygame.display.update()     
