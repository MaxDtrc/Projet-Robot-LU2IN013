import robot as driftator
from threading import Thread, enumerate

#Instantiation du controleur
controleur = driftator.ia.controleur()

#Definition de la "précision temporelle"
dT = 0.001

#Variables d'affichage
sim2d = False
sim3d = True

def chargerImplemVraieVie():
    #Initialisation du controleur
    implem = driftator.ia.implemVraiVie(driftator.ia.GetDecalageReel(driftator.ia.Variables(Robot2IN013())))

    ia = driftator.ia.openIA("test.ia", controleur, dT)
    ia.start()

def chargerImplemSimulation():
    #Creation du terrain
    simulation = driftator.simulation.chargerJson('config/config_immobile.json', dT)

    #Initialisation du controleur
    implem = driftator.ia.implemSimulation(driftator.ia.Variables(driftator.ia.GetDecalageSim(simulation.getRobot(0))), simulation)
    controleur.changerImplementation(implem)

    #Chargement de l'IA
    ia = driftator.ia.openIA("test.ia", controleur, dT)
    ia.start()

    #Initialisation de l'affichage
    if sim2d:
        affichage = driftator.affichage.Affichage(simulation, controleur,  360, 5, True, True)
    if sim3d:
        affichage3d = driftator.affichage.Affichage3d(simulation, controleur,  240)

    #Start des threads de la simulation
    simulation.start()

    #Start des thread de l'affichage
    if sim2d:
        affichage.start()
    if sim3d:
        affichage3d.start()
        affichage3d.app.run()


try:
    from robot2IN013 import Robot2IN013
    chargerImplemVraieVie()

except ImportError:
    chargerImplemSimulation()


