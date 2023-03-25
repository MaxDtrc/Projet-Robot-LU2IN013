def start(strat, dT = 0.001):
    from . import ia
    #Importation de la librairie du robot
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    controleur = ia.Controleur()
    implem = ia.implemVraiVie(ia.GetDecalageReel(ia.Variables(Robot2IN013())))
    controleur.changerImplem(implem)

    #Lancement de l'IA
    strat = ia.openIA("main_test_ia/"+strat, controleur, dT)
    strat.start()
