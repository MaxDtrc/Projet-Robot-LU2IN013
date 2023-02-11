import robot as r

#Initialisation du controleur
controleur = r.controleur()

try:
    from robot2IN013 import Robot2IN013
    implem = r.implemVraiVie(Robot2IN013())
    controleur.changerImplementation(implem)
except ImportError:
    import pygame
    import time
    import random

    #Definition de la taille du terrain
    tailleTerrainX = 510
    tailleTerrainY = 510

    #Definition de la "précision temporelle"
    dT = 0.1
        
    #Creation de la simulation
    simulation = r.Simulation(dT)

    #Creation du terrain
    simulation.chargerJson('test.json')

    #Initialisation de l'affichage
    a = r.Affichage(simulation, 60, 1.5, True)
    implem = r.implemSimulation(simulation.getRobot(0), simulation)
    controleur.changerImplementation(implem)
    simulation.start()
    a.start()  

ia = r.IA(controleur)
ia.start()