import robot as driftator
import os


#Instantiation du controleur
controleur = driftator.controleur()

#Definition de la taille du terrain
tailleTerrainX = 510
tailleTerrainY = 510

#Definition de la "précision temporelle"
dT = 0.01

#Chargement des configs
i = 1
select = -1
print("Liste des fichiers de config:")
for cfg in os.listdir('config'):
    print(str(i) + ": " + cfg[:-5])
    i += 1

while select < 1 or select > i:
    select = int(input("Choisissez la configuration à charger: "))


simulation = driftator.chargerJson("config/" + os.listdir('config')[select-1], dT)

#Initialisation de l'affichage
affichage = driftator.Affichage(simulation, 30, 1.5, False)

#Initialisation du controleur
implem = driftator.implemSimulation(simulation.getRobot(0), simulation)
controleur.changerImplementation(implem)

#Start des threads de la simulation
simulation.start()
affichage.start()  
