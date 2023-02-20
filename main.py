import robot as driftator

#Instantiation du controleur
controleur = driftator.ia.controleur()
dT = 0.001

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.ia.implemVraiVie(driftator.ia.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)

    def cond1(controleur):
        return controleur.getDistance() > 2
    
    def cond2(controleur):
        return controleur.getDistance() > 10

    strat1 = ([driftator.ia.IACondition(controleur, driftator.ia.AvancerDroit(controleur, 10, 270), driftator.ia.TournerDroite(controleur, 10, 50), cond2)], True) #Tourne quand près du mur
    strat2 = ([driftator.ia.IAWhile(controleur, driftator.ia.AvancerDroit(controleur, 10, 180), cond2)], True) #Avance vers le mur tant que pas trop près
    
    strat3 = ([driftator.ia.AvancerDroit(controleur, 10, 270), 
               driftator.ia.TournerGauche(controleur, 72, 270),
               driftator.ia.AvancerDroit(controleur, 10, 270),
               driftator.ia.TournerDroite(controleur, 144, 270)], True)
    
    strat4 = ([driftator.ia.ReculerDroit(controleur, 150, 270), driftator.ia.TournerDroite(controleur, 90, 180)], True)
    
    strats = [strat1, strat2, strat3, strat4]
    
except ImportError:
    #Definition de la "précision temporelle"
    

    #Creation du terrain
    simulation = driftator.simulation.chargerJson('config/config_immobile.json', dT)

    #Initialisation de l'affichage
    affichage = driftator.affichage.Affichage(simulation, 60, 4, True, True)

    #Initialisation du controleur
    implem = driftator.ia.implemSimulation(driftator.ia.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)


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
ia = driftator.ia.IA(controleur, strats[3], dT)
ia.start()
