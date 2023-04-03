#On modifie le main.py
#j'ai des soucis de parser quand il y a drawStop ou drawStart, j'ai pas le temps de les corriger

#1.1
simView = 1
strategie = "demo_ia/immobile.ia"
config = "config/config1.1.json"
#j'ai modifier config1.1, affichage.py
#immobile.ia est vide

#1.2
#j'ai modifier affichage.py

#1.3
#modifier controleur.py ajout dessine() et dans Variable() substituerVariables()

#1.4
simView = 1
strategie = "demo_ia/hexagone.ia"
config = "config/config_sans_obstacle.json"
#hexagone.ia


#2.1
simView = 1
strategie = "demo_ia/dessine1.ia"
config = "config/config_sans_obstacle.json"
#dessine1.ia

#2.2
simView = 1
strategie = "demo_ia/dessine0.ia"
config = "config/config_sans_obstacle.json"
#dessine0.ia

#2.3
simView = 1
strategie = "demo_ia/dessine01.ia"
config = "config/config_sans_obstacle.json"
#dessine01.ia

#2.4
simView = 1
strategie = "demo_ia/dessine01infini.ia"
config = "config/config_sans_obstacle.json"
#dessine01infini.ia

#3.1
#on considere que l'emmeteur est un mur de type 2
#dans objet.py

#3.2
#trouvesignal.ia

#3.3
#on va considere l'emmeteur comme un robot pour lui donner un deplacement plus facilement
#l'emmeteur est un robot avec l'iaemeteur.ia


#on modifie la ligne 134 de simulation.py pour qu'il affiche trouver au lieu de crash quand il va rentrer en collision avec l'emmeteur
#il peut detecter la collision entre deux robots