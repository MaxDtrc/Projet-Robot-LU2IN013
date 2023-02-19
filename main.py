import robot as driftator

#Instantiation du controleur
controleur = driftator.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.implemVraiVie(driftator.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)

    strats = [driftator.chargerIA("ia_carre.txt", controleur), driftator.chargerIA("ia_approcher_mur.txt", controleur)]
except ImportError:
    #Definition de la "précision temporelle"
    dT = 0.005

    #Creation du terrain
    simulation = driftator.chargerJson('config/config_immobile.json', dT)

    #Initialisation de l'affichage
    affichage = driftator.Affichage(simulation, 60, 5, True, True)

    #Initialisation du controleur
    implem = driftator.implemSimulation(driftator.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)


    def cond1(controleur):
        return controleur.getDistance() > 2
    
    def cond2(controleur):
        return controleur.getDistance() > 10

    strat1 = ([driftator.IACondition(controleur, driftator.AvancerDroit(controleur, 10, 270), driftator.TournerDroite(controleur, 10, 50), cond2)], True) #Tourne quand près du mur
    strat2 = ([driftator.IAWhile(controleur, driftator.AvancerDroit(controleur, 10, 270), cond1)], True) #Avance vers le mur tant que pas trop près
    
    strat3 = ([driftator.AvancerDroit(controleur, 30, 270), 
               driftator.TournerGauche(controleur, 72, 270),
               driftator.AvancerDroit(controleur, 30, 270),
               driftator.TournerDroite(controleur, 144, 270)], True)



    strats = [strat1, strat2, strat3]

    #Start des threads de la simulation
    simulation.start()
    affichage.start()


#Lancement de l'IA du robot
ia = driftator.IA(controleur, strats[2], dT)
ia.start()
