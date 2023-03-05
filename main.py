import robot as driftator
import time
#Instantiation du controleur
controleur = driftator.ia.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.ia.implemVraiVie(driftator.ia.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)

    strats = [(driftator.ia.Avancer(controleur, 100, 10), True)]
except ImportError:
    #Definition de la "précision temporelle"
    dT = 0.001

    #Creation du terrain
    simulation = driftator.simulation.chargerJson('config/config_immobile.json', dT)

    #Initialisation du controleur
    implem = driftator.ia.implemSimulation(driftator.ia.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)

    #Initialisation de l'affichage
    affichage = driftator.affichage.Affichage3d(simulation, controleur,  240)

    def cond(controleur):
        return controleur.getDistance() > 5
    
    ia = driftator.ia.IASeq(controleur, [driftator.ia.Avancer(controleur, 110, 900, -50), 
               driftator.ia.TournerSurPlace(controleur, -40, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300)])

    #Start des threads de la simulation
    simulation.start()
    affichage.start()


#Lancement de l'IA du robot
ia = driftator.ia.IA(controleur, ia, dT)
ia.start()
affichage.app.run()
