import robot as r
import os


#Instantiation du controleur
controleur = r.controleur()

#Definition de la taille du terrain
tailleTerrainX = 510
tailleTerrainY = 510

#Definition de la "précision temporelle"
dT = 0.01
        
#Creation de la simulation
s = r.Simulation(dT)

#Chargement des configs
i = 1
select = -1
print("Liste des fichiers de config:")
for cfg in os.listdir('config'):
    print(str(i) + ": " + cfg[:-5])
    i += 1

while select < 1 or select > i:
    select = int(input("Choisissez la configuration à charger: "))


s.chargerJson("config/" + os.listdir('config')[select-1], dT)

#Initialisation de l'affichage
a = r.Affichage(s, 30, 1.5, False)

#Initialisation du controleur
implem = r.implemSimulation(s.getRobot(0), s)
controleur.changerImplementation(implem)

#Start des threads de la simulation
s.start()
a.start()  