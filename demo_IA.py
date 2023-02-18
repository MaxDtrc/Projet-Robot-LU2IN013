import robot as driftator

#Instantiation du controleur
controleur = driftator.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.implemVraiVie(driftator.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)
except ImportError:
    #Choix de la stratégie
    select = -1
    print("Liste des stratégies:\n1: Tracer une carré (WIP)\n2: Approcher le mur")
    while select < 1 or select > 2:
        select = int(input("Choisissez la stratégie à charger: "))

    #Definition de la "précision temporelle"
    dT = 0.01

    #Creation du terrain
    simulation = driftator.chargerJson('config/config_immobile.json', dT)

    #Initialisation de l'affichage
    affichage = driftator.Affichage(simulation, 30, 5, False)

    #Initialisation du controleur
    implem = driftator.implemSimulation(driftator.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)

    strats = [driftator.chargerIA("ia_carre.txt", controleur), driftator.chargerIA("ia_approcher_mur.txt", controleur)]

    #Start des threads de la simulation
    simulation.start()
    affichage.start()  



#Lancement de l'IA du robot
ia = r.IA(controleur, strats[select - 1], dT)
ia.start()
