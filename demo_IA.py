import robot as driftator
import time

#Instantiation du controleur
controleur = driftator.ia.controleur()

#Definition de la "précision temporelle"
dT = 0.000001



#Choix de la stratégie
select = -1
print("Liste des stratégies:\n1: Evite les murs\n2: Approche du mur\n3: Dessine une étoile\n4: Dessine un carré\n5: Trace un cercle\n6: Dessin mystère")
while select < 1 or select > 7:
    select = int(input("Choisissez la stratégie à charger: "))


try:
    from robot2IN013 import Robot2IN013

    #Initialisation du controleur
    implem = driftator.ia.implemVraiVie(driftator.ia.GetDecalageReel(Robot2IN013()))
    controleur.changerImplementation(implem)

    controleur.start_recording()
    time.sleep(5)
except ImportError:
    

    #Creation du terrain
    simulation = driftator.simulation.chargerJson('config/config_immobile.json', dT)

    #Initialisation du controleur
    implem = driftator.ia.implemSimulation(driftator.ia.GetDecalageSim(simulation.getRobot(0)), simulation)
    controleur.changerImplementation(implem)

    #Initialisation de l'affichage
    affichage = driftator.affichage.Affichage(simulation, controleur,  240, 5, True, True)

    #Start des threads de la simulation
    simulation.start()
    affichage.start()  

#Lancement de l'IA du robot

#Liste des IA
def cond1(controleur):
    return controleur.getDistance() > 5
    
def cond2(controleur):
    return controleur.getDistance() > 50

def cond3(controleur):
    return controleur.getDistance() > 10

#Tourne quand près du mur
strat1 = ([driftator.ia.IACondition(controleur, driftator.ia.Avancer(controleur, 10, 600), driftator.ia.Avancer(controleur, 10, 900, 50), cond2)], True) 
    
#Avance vers le mur tant que pas trop près
strat2 = ([driftator.ia.IAWhile(controleur, driftator.ia.Avancer(controleur, 100, 180), cond1)], True) 
    
#Dessine une étoile
strat3 = ([driftator.ia.Avancer(controleur, 20, 180), 
            driftator.ia.TournerSurPlace(controleur, -72, 270),
            driftator.ia.Avancer(controleur, 20, 180),
            driftator.ia.TournerSurPlace(controleur, 144, 270)], True)
    
#Dessine un carré
strat4 = ([driftator.ia.Avancer(controleur, 20, 180),
           driftator.ia.TournerSurPlace(controleur, 90, 180)],True)
    
#Trace un cercle
strat5 = ([driftator.ia.Avancer(controleur, 100, 360, -40)], True)

#Trace un dessin mystère
strat6 = ([driftator.ia.Avancer(controleur, 110, 360, -50), 
            driftator.ia.TournerSurPlace(controleur, -40, 300),
            driftator.ia.Avancer(controleur, 42, 360, -50),
            driftator.ia.TournerSurPlace(controleur, -80, 300),
            driftator.ia.Avancer(controleur, 42, 360, -50),
            driftator.ia.TournerSurPlace(controleur, -80, 300),
            driftator.ia.Avancer(controleur, 42, 360, -50),
            driftator.ia.TournerSurPlace(controleur, -80, 300),
            driftator.ia.Avancer(controleur, 42, 360, -50),
            driftator.ia.TournerSurPlace(controleur, -80, 300),
            driftator.ia.Avancer(controleur, 42, 360, -50),
            driftator.ia.TournerSurPlace(controleur, -80, 300)], False)

#Approche du mur, puis fait un 360
strat7 = ([driftator.ia.IAWhile(controleur, driftator.ia.Avancer(controleur, 200, 180), cond3), 
           driftator.ia.TournerSurPlace(controleur, 180, 180),
           driftator.ia.IAWhile(controleur, driftator.ia.Avancer(controleur, 200, 180), cond3), 
           driftator.ia.TournerSurPlace(controleur, -180, 180)], True)


strat7 = ([driftator.ia.Avancer(controleur, 1, 45)], False)
    
strats = [strat1, strat2, strat3, strat4, strat5, strat6, strat7]

    
ia = driftator.ia.IA(controleur, strats[select - 1], dT)
ia.start()
