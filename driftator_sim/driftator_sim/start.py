def start(strat, config, simView = 1, dT = 0.0001):
    import driftator
    from . import simulation, affichage, ia
    
    #Creation de la simulation
    simulation = simulation.chargerJson(config, dT)

    #Initialisation du controleur
    controleur = driftator.ia.controleur()
    implem = ia.implemSimulation(driftator.ia.Variables(ia.GetDecalageSim(simulation.getRobot(0))), simulation)
    controleur.changerImplementation(implem)

    #Chargement de l'IA
    strat = driftator.ia.openIA(strat, controleur, dT)
    strat.start()

    #Initialisation de l'affichage
    if simView == 1:
        affichage2d = affichage.Affichage(simulation, controleur,  360, 5, True, True)
    elif simView == 2:
        affichage3d = affichage.Affichage3d(simulation, controleur,  240)
        controleur.set_a(affichage3d)
        
    #Start des threads de la simulation
    simulation.start()

    #Lancement de l'affichage (dans le thread principal)
    if simView == 1:
        affichage2d.run()
    elif simView == 2:
        affichage3d.start()
        affichage3d.app.run()
