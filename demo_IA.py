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
    print("Liste des stratégies:\n1: Evite les murs\n2: Approche du mur\n3: Dessine une étoile\n4: Dessine un carré\n5: Trace un cercle\n6: Dessin mystère")
    while select < 1 or select > 6:
        select = int(input("Choisissez la stratégie à charger: "))

    #Definition de la "précision temporelle"
    dT = 0.005

    #Creation du terrain
    simulation = driftator.simulation.chargerJson('config/config_immobile.json', dT)

    #Initialisation du controleur
    implem = driftator.ia.implemSimulation(driftator.ia.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)

    #Initialisation de l'affichage
    affichage = driftator.affichage.Affichage(simulation, controleur,  240, 5, True, True)

    
    #Liste des IA
    def cond1(controleur):
        return controleur.getDistance() > 2
    
    def cond2(controleur):
        return controleur.getDistance() > 50

    #Tourne quand près du mur
    strat1 = ([driftator.ia.IACondition(controleur, driftator.ia.Avancer(controleur, 10, 600), driftator.ia.Avancer(controleur, 10, 900, 50), cond2)], True) 
    
    #Avance vers le mur tant que pas trop près
    strat2 = ([driftator.ia.IAWhile(controleur, driftator.ia.Avancer(controleur, 10, 270), cond1)], True) 
    
    #Dessine une étoile
    strat3 = ([driftator.ia.Avancer(controleur, 30, 270), 
               driftator.ia.TournerSurPlace(controleur, -72, 270),
               driftator.ia.Avancer(controleur, 30, 270),
               driftator.ia.TournerSurPlace(controleur, 144, 270)], True)
    
    #Dessine un carré
    strat4 = ([driftator.ia.Avancer(controleur, 30, 270), 
               driftator.ia.TournerSurPlace(controleur, -90, 270)], True)
    
    #Trace un cercle
    strat5 = ([driftator.ia.Avancer(controleur, 10, 270, -40)], True)

    #Trace un dessin mystère
    strat6 = ([driftator.ia.Avancer(controleur, 110, 900, -50), 
               driftator.ia.TournerSurPlace(controleur, -40, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300),
               driftator.ia.Avancer(controleur, 42, 900, -50),
               driftator.ia.TournerSurPlace(controleur, -80, 300)], False)
    
    strats = [strat1, strat2, strat3, strat4, strat5, strat6]

    #Start des threads de la simulation
    simulation.start()
    affichage.start()  

#Lancement de l'IA du robot
ia = driftator.ia.IA(controleur, strats[select - 1], dT)
ia.start()
