def startRobot(strat, dT = 0.001):
    from . import ia
    #Importation de la librairie du robot
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    controleur = ia.Variables(ia.controleur())
    implem = ia.implemVraiVie(ia.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)

    #Lancement de l'IA
    #strat = ia.openIA("demo_ia/"+strat, controleur, dT)
    strat = ia.openIA(strat, controleur, dT)
    strat.start()


def startSimulation(strat, config, simView = 1, dT = 0.0001, emetteur = False, deplacerEmetteur = False):
    from . import simulation, affichage, ia
    #Creation de la simulation
    sim = simulation.chargerJson(config, dT)

    sim.deplacerEmetteur = deplacerEmetteur

    if(emetteur):
        #Création de l'emetteur
        from random import randint
        e = simulation.Emetteur("emetteur", randint(-70, 70), randint(-70, 70), 3)
        sim.terrain.ajouterObstacle(e)

    for i in range(0, sim.getNombreDeRobots()):
        #Initialisation du controleur
        controleur = ia.Variables(ia.controleur())
        implem = ia.implemSimulation(ia.GetDecalageSim(sim.getRobot(i)), sim)
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
