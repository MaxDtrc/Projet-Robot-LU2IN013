import pygame
import random

import Objets as o
import Simulation as s

class Affichage :

    def __init__(self, simulation : s.Simulation):
        pygame.init()
        self._screen = pygame.display.set_mode((simulation.getTerrain().getSizeX(), simulation.getTerrain().getSizeY()))
        pygame.display.set_caption('Test de la simulation du robot') 
        self._screen.fill((255,255,255))

    def afficherObstacles(obstacle : o.Obstacle, screen):
        if (isinstance(obstacle, o.ObstacleCarre)):
            pygame.draw.rect(screen, (255,0,0), (obstacle.getX(),obstacle.getY(),obstacle.getLongueur(),obstacle.getLongueur()))
        elif (isinstance(obstacle, o.ObstacleRond)):
            pygame.draw.circle(screen, (255,0,0), (obstacle.getX(), obstacle.getY()), obstacle.getRayon())



    def afficherRobots(robot: o.Robot, screen):
        #Image de base
        image_pas_tournee = pygame.image.load("robot.png").convert_alpha()
        #Image que l'on tourne en fonction de l'angle du robot
        image = pygame.transform.rotate(image_pas_tournee, robot.getAngle())
        #Affichage du robot sur le screen
        screen.blit(image, (tailleTerrainX/2 - image.get_width()/2 + robot.getX(), tailleTerrainY/2 - image.get_height()/2 + robot.getY()))



    def afficherSimulation(simulation : s.Simulation, screen):


        #Initialisation de la fenêtre pygame
        


    
