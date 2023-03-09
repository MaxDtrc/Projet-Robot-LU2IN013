import robot as driftator
import time
#Instantiation du controleur
controleur = driftator.ia.controleur()


#Definition de la "précision temporelle"
dT = 0.000001

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.ia.implemVraiVie(driftator.ia.GetDecalageReel(driftator.ia.Variables(Robot2IN013())))

    def cond(controleur):
        return True
    
    ia = driftator.ia.openIA("test.ia", controleur, dT)
    ia.start()

except ImportError:
    #Creation du terrain
    simulation = driftator.simulation.chargerJson('config/config_immobile.json', dT)

    #Initialisation du controleur
    implem = driftator.ia.implemSimulation(driftator.ia.Variables(driftator.ia.GetDecalageSim(simulation.getRobot(0))), simulation)
    controleur.changerImplementation(implem)

    ia = driftator.ia.openIA("test.ia", controleur, dT)
    ia.start()

    #Initialisation de l'affichage
    affichage = driftator.affichage.Affichage(simulation, controleur,  360, 5, True, True)
    #affichage3d = driftator.affichage.Affichage3d(simulation, controleur,  240)

    def cond(controleur):
        return True
    
    ia = driftator.ia.IAWhile(controleur, driftator.ia.IASeq(controleur, [driftator.ia.Avancer(controleur, 50, 900, 0), 
               driftator.ia.TournerSurPlace(controleur, 90, 60)]), cond)

    #Start des threads de la simulation
    simulation.start()
    affichage.start()
    #affichage3d.start()
    #affichage3d.app.run()
