import robot as driftator

#Instantiation du controleur
controleur = driftator.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.implemVraiVie(driftator.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)

    strats = [driftator.chargerIA("ia_carre.txt", controleur), driftator.chargerIA("ia_approcher_mur.txt", controleur)]
except ImportError:
    #Definition de la "précision temporelle"
    dT = 0.01

    #Creation du terrain
    simulation = driftator.chargerJson('config/config_immobile.json', dT)

    #Initialisation de l'affichage
    affichage = driftator.Affichage(simulation, 30, 5, True)

    #Initialisation du controleur
    implem = driftator.implemSimulation(driftator.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)

    strats = [driftator.chargerIA(controleur, "ia_carre.txt"), driftator.chargerIA(controleur, "ia_approcher_mur.txt")]

    #Start des threads de la simulation
    simulation.start()
    affichage.start()




#Lancement de l'IA du robot
ia = r.IA(controleur, strats[1], dT)
ia.start()
