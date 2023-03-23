import driftator

#Instantiation du controleur
controleur = driftator.ia.controleur()

#Definition de la "précision temporelle"
dT = 0.001

#Variables d'affichage (1 = 2d, 2 = 3d)
simView = 1

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
    ia = driftator.ia.openIA("test2.ia", controleur, dT)
    ia.start()

    #Initialisation de l'affichage
    if simView == 1:
        affichage2d = driftator.affichage.Affichage(simulation, controleur,  360, 5, True, False)
    elif simView == 2:
        affichage3d = driftator.affichage.Affichage3d(simulation, controleur,  240)
        controleur.set_a(affichage3d)
        
    #Start des threads de la simulation
    simulation.start()

    #Lancement de l'affichage (dans le thread principal)
    if simView == 1:
        affichage2d.run()
    elif simView == 2:
        affichage3d.start()
        affichage3d.app.run()
    
        
try:
    from robot2IN013 import Robot2IN013
    chargerImplemVraieVie()

except ImportError:
    chargerImplemSimulation()
    


