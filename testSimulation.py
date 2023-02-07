import robot as r

import time
import pygame
import random


#Definition de la taille du terrain
tailleTerrainX = 510
tailleTerrainY = 510
    
#Creation de la simulation
simulation = r.Simulation()

#Creation du terrain
terrain = r.Terrain(tailleTerrainX,tailleTerrainY)
terrain.ajouterObstacle(r.ObstacleRond("rond1", 100, 80, 50))
terrain.ajouterObstacle(r.ObstacleRond("rond1", -100, -80, 50))

terrain.ajouterObstacle(r.ObstacleRectangle("carre1", 150, -80, 60, 60))
terrain.ajouterObstacle(r.ObstacleRectangle("carre2", -150, 80, 60, 60))

terrain.ajouterObstacle(r.ObstacleRectangle("mur1", 249, 0, 3, 500))
terrain.ajouterObstacle(r.ObstacleRectangle("mur2", -249, 0, 3, 500))
terrain.ajouterObstacle(r.ObstacleRectangle("mur3", 0, 249, 500, 3))
terrain.ajouterObstacle(r.ObstacleRectangle("mur4", 0, -249, 500, 3))

simulation.setTerrain(terrain)

#Initialisation de l'affichage
a = r.Affichage(simulation, 1.5)

#Definition de la "précision temporelle"
dT = 0.1

#Boucle principale
enMarche = True
while enMarche:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enMarche = False
        
    #Apparition d'un robot si aucun présent
    if(simulation.getNombreDeRobots() == 0):
        simulation.ajouterRobot(r.Robot("robot", 0, 0, random.randint(0, 360), 7, 15, 100))

    simulation.actualiser(dT) #Actualisation de la simulation
    a.afficherSimulation(simulation) #Affichage de la simulation
    time.sleep(dT)

