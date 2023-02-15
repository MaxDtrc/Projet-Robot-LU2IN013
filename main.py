import robot as r

#Instantiation du controleur
controleur = r.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = r.implemVraiVie(r.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)

    strats = [r.chargerIA("ia_carre.txt", controleur), r.chargerIA("ia_approcher_mur.txt", controleur)]
except ImportError:
    #Definition de la "précision temporelle"
    dT = 0.01

    #Creation du terrain
    s = r.chargerJson('config/config_immobile.json', dT)

    #Initialisation de l'affichage
    a = r.Affichage(s, 30, 5, True)

    #Initialisation du controleur
    implem = r.implemSimulation(r.GetDecalageSim(s.getRobot(0)), s)
    controleur.changerImplementation(implem)

    strats = [r.chargerIA(controleur, "ia_carre.txt"), r.chargerIA(controleur, "ia_approcher_mur.txt")]

    #Start des threads de la simulation
    s.start()
    a.start()




#Lancement de l'IA du robot
ia = r.IA(controleur, strats[1], dT)
ia.start()