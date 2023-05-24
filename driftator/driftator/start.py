def startRobot(strat, dT = 0.001):
    from . import ia
    #Importation de la librairie du robot
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    controleur = ia.Variables(ia.controleur())
    implem = ia.implemVraiVie(ia.GetDecalage(Robot2IN013()))
    controleur.changerImplementation(implem)

    #Lancement de l'IA
    strat = ia.openIA(strat, controleur, dT)
    strat.start()


def startSimulation(strat, config, simView = 1, dT = 0.00001):
    from . import simulation, affichage, ia
    
    #Creation de la simulation
    sim = simulation.chargerJson(config, dT)

    for i in range(0, sim.getNombreDeRobots()):
        #Initialisation du controleur
        controleur = ia.Variables(ia.controleur())
        implem = ia.implemSimulation(ia.GetDecalage(sim.getRobot(i)), sim)
        controleur.changerImplementation(implem)
        #Chargement de l'IA
        strategie = ia.openIA(strat, controleur, dT)
        strategie.start()

    #Initialisation de l'affichage
    if simView == 1:
        affichage2d = affichage.Affichage(sim, controleur,  360, 5, True, True)
    elif simView == 2:
        affichage3d = affichage.Affichage3d(sim, controleur,  240)
        controleur.set_a(affichage3d)
        
    #Start des threads de la simulation
    sim.start()

    #Lancement de l'affichage (dans le thread principal)
    if simView == 1:
        affichage2d.run()
    elif simView == 2:
        affichage3d.start()
        affichage3d.app.run()
