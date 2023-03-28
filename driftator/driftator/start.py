def start(strat, dT = 0.1):
    from . import ia
    #Importation de la librairie du robot
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    controleur = ia.controleur()
    implem = ia.implemVraiVie(ia.GetDecalageReel(ia.Variables(Robot2IN013())))
    controleur.changerImplementation(implem)

    #Lancement de l'IA
    #strat = ia.openIA("demo_ia/"+strat, controleur, dT)
    strat = ia.openIA(strat, controleur, dT)
    strat.start()
