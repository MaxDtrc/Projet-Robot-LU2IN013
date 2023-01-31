import Simulation as s
import Objets as o
import Affichage as af

import time
import pygame
import random


#Definition de la taille du terrain
tailleTerrainX = 500
tailleTerrainY = 500
    
#Creation de la simulation
simulation = s.Simulation()

#Creation du terrain
terrain = o.Terrain(tailleTerrainX,tailleTerrainY)
terrain.ajouterObstacle(o.ObstacleRond("obs1", 150, 80, 50))
terrain.ajouterObstacle(o.ObstacleRectangle("obs2", 249, 0, 3, 500))
terrain.ajouterObstacle(o.ObstacleRectangle("obs3", -249, 0, 3, 500))
terrain.ajouterObstacle(o.ObstacleRectangle("obs4", 0, 249, 500, 3))
terrain.ajouterObstacle(o.ObstacleRectangle("obs4", 0, -249, 500, 3))

simulation.setTerrain(terrain)

#Ajout d'un robot
simulation.ajouterRobot(o.Robot("robot", random.randint(-tailleTerrainX/2,tailleTerrainX/2), random.randint(-tailleTerrainY/2,tailleTerrainY/2), random.randint(0, 360), 10, 100))

#Initialisation de l'affichage
a = af.Affichage(simulation)

#Definition de la "précision temporelle"
dT = 0.1

#Boucle principale
enMarche = True
while enMarche:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enMarche = False
        
        
    simulation.actualiser(dT) #Actualisation de la simulation
    a.afficherSimulation(simulation) #Affichage de la simulation
    time.sleep(dT)