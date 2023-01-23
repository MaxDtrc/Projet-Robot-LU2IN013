from Simulation import Simulation
from Robot import Robot
from Terrain import Terrain

import time
import pygame
import random

def testSimulation():
    
    #Initialisation du terrain et de la simulation

    tailleTerrainX = 500
    tailleTerrainY = 500

    simulation = Simulation()

    terrain = Terrain(tailleTerrainX,tailleTerrainY)

    simulation.setTerrain(terrain)

    for i in range(10):
        simulation.ajouterRobot(Robot("robot", random.randint(-tailleTerrainX/2,tailleTerrainX/2), random.randint(-tailleTerrainY/2,tailleTerrainY/2), random.randint(0, 360)))
    

    #Initialisation de la fenêtre pygame

    pygame.init()

    screen = pygame.display.set_mode((tailleTerrainX, tailleTerrainY))

    pygame.display.set_caption('Test de la simulation du robot') 

    image = pygame.image.load("robot.png").convert_alpha()

    # attends jusqu'à ce que l'utilisateur ferme la fenêtre
    enMarche = True
    while enMarche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                enMarche = False
        screen.fill((255,255,255))
        pygame.display.update()

        for robot in simulation.getRobotsList():
            screen.blit(image, (tailleTerrainX/2 - image.get_width()/2 + robot.getX(), tailleTerrainY/2 - image.get_height()/2 + robot.getY()))
            if(robot.getDistanceFromRobot(terrain) < 20):
                robot.tourner(90)
                image = pygame.transform.rotate(image, robot.getAngle())
            robot.avancer(100)
        pygame.display.update()



        time.sleep(1)


   



testSimulation()
    
