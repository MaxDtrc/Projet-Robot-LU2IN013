import robot as r

#Instantiation du controleur
controleur = r.controleur()

try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = r.implemVraiVie(Robot2IN013())
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
    s = r.chargerJson('config/config_immobile.json', dT)

    #Initialisation de l'affichage
    a = r.Affichage(s, 30, 5, True)

    #Initialisation du controleur
    implem = r.implemSimulation(s.getRobot(0), s)
    controleur.changerImplementation(implem)

    strats = [([r.AvancerDroit(controleur, 50, 720), r.TournerDroite(controleur, 90, 45)], True), ([r.ApprocherMur(controleur, 2)], False)]

    #Start des threads de la simulation
    s.start()
    a.start()  



#Lancement de l'IA du robot
ia = r.IA(controleur, strats[select - 1], dT)
ia.start()