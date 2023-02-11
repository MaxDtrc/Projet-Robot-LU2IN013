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
simulation.chargerJson('test.json')

#Initialisation de l'affichage
a = r.Affichage(simulation, 60, 1.5, True)

#Definition de la "précision temporelle"
dT = 0.1

a.start()

#Boucle principale
enMarche = True
while enMarche:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            enMarche = False
        
    #Apparition d'un robot si aucun présent
    if(simulation.getNombreDeRobots() == 0):
        simulation.ajouterRobot(r.Robot("robot", 0, 0, random.randint(0, 360), 7, 15, 10000))

    simulation.actualiser(dT) #Actualisation de la simulation
    time.sleep(dT)

