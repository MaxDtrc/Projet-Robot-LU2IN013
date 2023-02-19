import robot as driftator

#Instantiation du controleur
controleur = driftator.ia.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.ia.implemVraiVie(driftator.ia.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)
except ImportError:
    #Choix de la stratégie
    select = -1
    print("Liste des stratégies:\n1: Approcher mur\n2: Evite les murs\n3: Dessine une étoile")
    while select < 1 or select > 3:
        select = int(input("Choisissez la stratégie à charger: "))

    #Definition de la "précision temporelle"
    dT = 0.01

    #Creation du terrain
    simulation = driftator.simulation.chargerJson('config/config_immobile.json', dT)

    #Initialisation de l'affichage
    affichage = driftator.affichage.Affichage(simulation, 60, 5, False, True)

    #Initialisation du controleur
    implem = driftator.ia.implemSimulation(driftator.ia.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)

    def cond1(controleur):
        return controleur.getDistance() > 2
    
    def cond2(controleur):
        return controleur.getDistance() > 10

    strat1 = ([driftator.ia.IACondition(controleur, driftator.ia.AvancerDroit(controleur, 10, 270), driftator.ia.TournerDroite(controleur, 10, 50), cond2)], True) #Tourne quand près du mur
    strat2 = ([driftator.ia.IAWhile(controleur, driftator.ia.AvancerDroit(controleur, 10, 270), cond1)], True) #Avance vers le mur tant que pas trop près
    strat3 = ([driftator.ia.AvancerDroit(controleur, 30, 270), driftator.ia.TournerGauche(controleur, 72, 270), driftator.ia.AvancerDroit(controleur, 30, 270), driftator.ia.TournerDroite(controleur, 144, 270)], True)

    strats = [strat1, strat2, strat3]

    #Start des threads de la simulation
    simulation.start()
    affichage.start()  



#Lancement de l'IA du robot
ia = driftator.ia.IA(controleur, strats[select - 1], dT)
ia.start()
