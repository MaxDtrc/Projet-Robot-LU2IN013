import json

def startRobot(strat, dT = 0.001):
    """
    Fonction permettant de lancer le robot irl avec une certaine stratégie (ia)
    :param strat: la stratégie choisie pour l ia 
    :param dT: dT choisi pour l actualisation dans le fichier settings.json
    """
    from . import ia

    #Importation de la librairie du robot
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    controleur = ia.Variables(ia.controleur())
    implem = ia.implemVraiVie(ia.GetDecalage(Robot2IN013()))
    controleur.changerImplementation(implem)

    #Chargement des paramètres
    with open("settings.json", "r") as json_file:
        data = json.load(json_file)

    #Lancement de l'IA
    strat = ia.openIA(strat, controleur, data["general"]["dTRobot"])
    strat.start()


def startSimulation(strat, config, simView = 1, dT = 0.00001):
    """
    Fonction permettant de lancer la simulation du robot en 2D ou 3D avec une config et une stratégie
    :param strat: la stratégie (ia) choisie
    :param config: le fichier de configuration choisi
    :param simView: 1=vue 2D / 2=vue 3D
    :param dT: dT choisi pour l actualisation dans le fichier settings.json
    """
    from . import simulation, affichage, ia

    #Chargement des paramètres
    with open("settings.json", "r") as json_file:
        data = json.load(json_file)
    
    #Creation de la simulation
    sim = simulation.chargerJson(config, data["general"]["dTSimu"])

    for i in range(0, sim.getNombreDeRobots()):
        #Initialisation du controleur
        controleur = ia.Variables(ia.controleur())
        implem = ia.implemSimulation(ia.GetDecalage(sim.getRobot(i)), sim)
        controleur.changerImplementation(implem)
        #Chargement de l'IA
        strategie = ia.openIA(strat, controleur, data["general"]["dTSimu"])
        strategie.start()

    #Initialisation de l'affichage
    if simView == 1:
        affichage2d = affichage.Affichage(sim, controleur,  data["affichage2d"]["fps"], data["affichage2d"]["echelle"], data["affichage2d"]["afficherDistance"], data["affichage2d"]["afficherTrace"])
    elif simView == 2:
        affichage3d = affichage.Affichage3d(sim, controleur,  data["affichage3d"]["fps"])
        controleur.set_a(affichage3d)
        
    #Start des threads de la simulation
    sim.start()

    #Lancement de l'affichage (dans le thread principal)
    if simView == 1:
        affichage2d.run()
    elif simView == 2:
        affichage3d.start()
        affichage3d.app.run()
