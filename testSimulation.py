import SimulationClasse as s
import Objets as o


import time
import pygame
import random

def testSimulation():
    
    #Initialisation du terrain et de la simulation

    tailleTerrainX = 500
    tailleTerrainY = 500

    simulation = s.Simulation()

    terrain = o.Terrain(tailleTerrainX,tailleTerrainY)

    simulation.setTerrain(terrain)

    for i in range(1):
        #simulation.ajouterRobot(o.Robot("robot", random.randint(-tailleTerrainX/2,tailleTerrainX/2), random.randint(-tailleTerrainY/2,tailleTerrainY/2), random.randint(0, 360)))
        simulation.ajouterRobot(o.Robot("robot", 0,0, 90, 10, 200))
    

    #Initialisation de la fenêtre pygame

    pygame.init()

    screen = pygame.display.set_mode((tailleTerrainX, tailleTerrainY))

    pygame.display.set_caption('Test de la simulation du robot') 

    image_pas_tournee = pygame.image.load("robot.png").convert_alpha()

    obstacle = o.ObstacleCarre("obs", 4, 4, 3)

    # attends jusqu'à ce que l'utilisateur ferme la fenêtre
    enMarche = True
    while enMarche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                enMarche = False
        screen.fill((255,255,255))

        for robot in simulation.getRobotsList():
            image = pygame.transform.rotate(image_pas_tournee, robot.getAngle())
            screen.blit(image, (tailleTerrainX/2 - image.get_width()/2 + robot.getX(), tailleTerrainY/2 - image.get_height()/2 + robot.getY()))
            pygame.draw.rect(screen, (255,0,0), (4,4,10,10))
            simulation.actualiser(0.1)
        
        pygame.display.update()
        time.sleep(0.1)

testSimulation()
    
