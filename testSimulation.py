import Simulation as s
import Objets as o
import Affichage as a

import time
import pygame
import random

def testSimulation():

    tailleTerrainX = 500
    tailleTerrainY = 500
    
    #Initialisation de nos variables
    simulation = s.Simulation()
    terrain = o.Terrain(tailleTerrainX,tailleTerrainY)
    simulation.setTerrain(terrain)

    


    #Ajout des robots
    for i in range(1):
        simulation.ajouterRobot(o.Robot("robot", random.randint(-tailleTerrainX/2,tailleTerrainX/2), random.randint(-tailleTerrainY/2,tailleTerrainY/2), random.randint(0, 360)))
    
    #Ajout des obstacles TODO
    obstacle = o.ObstacleRond("obs", 150, 80, 50)


    # attends jusqu'à ce que l'utilisateur ferme la fenêtre
    enMarche = True
    while enMarche:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                enMarche = False


        """
        screen.fill((255,255,255))

        for robot in simulation.getRobotsList():
            image = pygame.transform.rotate(image_pas_tournee, robot.getAngle())
            screen.blit(image, (tailleTerrainX/2 - image.get_width()/2 + robot.getX(), tailleTerrainY/2 - image.get_height()/2 + robot.getY()))
            #pygame.draw.rect(screen, (255,0,0), (4,4,10,10))
            a.afficherObstacles(obstacle, screen)
            simulation.actualiserSimulation(0.1)"""
        
        pygame.display.update()
        time.sleep(0.1)

testSimulation()
    
