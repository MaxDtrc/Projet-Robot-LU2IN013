import simulation as s
import objets as o
import affichage as af

import time
import pygame
import random


#Definition de la taille du terrain
tailleTerrainX = 700
tailleTerrainY = 700
    
#Creation de la simulation
simulation = s.Simulation()

#Creation du terrain
terrain = o.Terrain(tailleTerrainX,tailleTerrainY)
terrain.ajouterObstacle(o.ObstacleRond("rond1", 100, 80, 50))
terrain.ajouterObstacle(o.ObstacleRond("rond1", -100, -80, 50))

terrain.ajouterObstacle(o.ObstacleRectangle("carre1", 150, -80, 60, 60))
terrain.ajouterObstacle(o.ObstacleRectangle("carre2", -150, 80, 60, 60))

terrain.ajouterObstacle(o.ObstacleRectangle("mur1", 249, 0, 3, 500))
terrain.ajouterObstacle(o.ObstacleRectangle("mur2", -249, 0, 3, 500))
terrain.ajouterObstacle(o.ObstacleRectangle("mur3", 0, 249, 500, 3))
terrain.ajouterObstacle(o.ObstacleRectangle("mur4", 0, -249, 500, 3))

simulation.setTerrain(terrain)

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
        
    #Apparition d'un robot si aucun présent
    if(simulation.getNombreDeRobots() == 0):
        simulation.ajouterRobot(o.Robot("robot", 0, 0, random.randint(0, 360), 15, 100))

    simulation.actualiser(dT) #Actualisation de la simulation
    a.afficherSimulation(simulation) #Affichage de la simulation
    time.sleep(dT)

