import robot as driftator

#Instantiation du controleur
controleur = driftator.ia.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.ia.implemVraiVie(driftator.ia.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)

    strats = [(driftator.ia.AvancerDroit(controleur, 100, 10), True)]
except ImportError:
    #Definition de la "précision temporelle"
    dT = 0.005

    #Creation du terrain
    simulation = driftator.simulation.chargerJson('config/config_immobile.json', dT)

    #Initialisation du controleur
    implem = driftator.ia.implemSimulation(driftator.ia.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)

    #Initialisation de l'affichage
    affichage = driftator.affichage.Affichage(simulation, controleur,  60, 5, True, True)

    def cond1(controleur):
        return controleur.getDistance() > 2
    
    def cond2(controleur):
        return controleur.getDistance() > 10

    strat1 = ([driftator.ia.IACondition(controleur, driftator.ia.AvancerDroit(controleur, 10, 270), driftator.ia.TournerDroite(controleur, 10, 50), cond2)], True) #Tourne quand près du mur
    strat2 = ([driftator.ia.IAWhile(controleur, driftator.ia.AvancerDroit(controleur, 10, 270), cond1)], True) #Avance vers le mur tant que pas trop près
    
    strat3 = ([driftator.ia.AvancerDroit(controleur, 30, 270), 
               driftator.ia.TournerGauche(controleur, 72, 270),
               driftator.ia.AvancerDroit(controleur, 30, 270),
               driftator.ia.TournerDroite(controleur, 144, 270)], True)



    strats = [strat1, strat2, strat3]

    #Start des threads de la simulation
    simulation.start()
    affichage.start()


#Lancement de l'IA du robot
ia = driftator.ia.IA(controleur, strats[2], dT)
ia.start()
