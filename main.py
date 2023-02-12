import robot as r

#Instantiation du controleur
controleur = r.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = r.implemVraiVie(Robot2IN013())
    controleur.changerImplementation(implem)
except ImportError:
    #Definition de la taille du terrain
    tailleTerrainX = 510
    tailleTerrainY = 510

    #Definition de la "précision temporelle"
    dT = 0.1
        
    #Creation de la simulation
    s = r.Simulation(dT)

    #Creation du terrain
    s.chargerJson('config/config_immobile.json')

    #Initialisation de l'affichage
    a = r.Affichage(s, 60, 1.5, True)

    #Initialisation du controleur
    implem = r.implemSimulation(s.getRobot(0), s)
    controleur.changerImplementation(implem)

    #Start des threads de la simulation
    s.start()
    a.start()  

#Lancement de l'IA du robot
ia = r.IA(controleur)
ia.start()