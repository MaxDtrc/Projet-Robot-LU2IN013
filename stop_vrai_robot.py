import robot as driftator

#Instantiation du controleur
controleur = driftator.ia.controleur()

#Definition de la "précision temporelle"
dT = 0.005



from robot2IN013 import Robot2IN013

#Initialisation du controleur
implem = driftator.ia.implemVraiVie(driftator.ia.GetDecalageReel(Robot2IN013()))
controleur.changerImplementation(implem)

controleur.setVitesseGauche(0)
controleur.setVitesseDroite(0)