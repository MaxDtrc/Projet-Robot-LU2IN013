import Objets as o
from math import cos, sin, radians, degrees


class Simulation : 
    """
    Classe représentant la simulation
    """

    def __init__(self, robotsList : list = None, terrain : o.Terrain = None):
        """
        Constructeur de la classe Simulation

        Paramètres:
        robotsList -> Liste de robots
        terrain -> Le terrain
        """
        
        if robotsList is None : 
            self._robotsList = []
        else:
            self._robotsList = robotsList
        self._terrain = terrain
    

    def ajouterRobot(self, robot : o.Robot):
        """
        Ajoute un robot dans la liste des robots de la simulation

        Paramètres:
        robot -> le robot à ajouter dans la liste
        """

        self._robotsList.append(robot)

    
    def retirerRobot(self, robot : o.Robot):
        """
        Retire le robot passé en paramètre de la liste des robots de la simulation

        Paramètres:
        robot -> le robot à retirer de la liste
        """

        self._robotList.remove(robot)


    def retirerRobot(self, index : int):
        """
        Retire le robot à l'index passé en paramètre de la liste de robots de la simulation 

        Paramètres:
        index -> l'index du robot à enlever
        """
        self._robotsList.pop(index)

    def setTerrain(self, terrain : o.Terrain):
        """
        Affecte le terrain passé en paramètre à la variable Terrain de la simulation

        Paramètres:
        terrain -> le terrain à affecter
        """

        self._terrain = terrain

    def getTerrain(self):
        """
        Renvoie le Terrain affecté à la variable Terrain de la simulation

        """

        return self._terrain

    def getRobotsList(self):
        """
        Renvoie la liste contenant tout les robots de la simulation

        """
        
        return self._robotsList

    def getRobot(self, index : int):
        """
        Renvoie le robot correspondant à l'index passé en paramètre dans le tableau de robots

        Paramètres:
        index -> l'index du robot à renvoyer
        """

        return self._robotsList[index]


    def afficherSimulation(self, screen):
        """
        Affiche l'ensemble de la simulation grâce à la librairie graphique (pour l'instant tous les robots de la liste)

        Paramètres:
        robotsList -> la liste des robots à afficher
        """

        for robot in self._robotsList :
            robot.afficher(screen)
        
    #Capteur de distance
    def getDistanceFromRobot(self, robot: o.Robot):
        """
        Renvoie la distance jusqu'au prochain mur
        
        Paramètres:
        terrain -> Terrain
        """
        dirVect = (cos(radians(robot.getAngle())), sin(radians(robot.getAngle())))
        posRayon = (robot.getX(), robot.getY())
        distance = 0

        while distance < self._terrain.getSizeX() * self._terrain.getSizeY(): #Limite pour pas que le rayon n'avance à l'infini
            #Detection des bords du terrain
            if(abs(posRayon[0]) >= self._terrain.getSizeX()/2 or abs(posRayon[1]) >= self._terrain.getSizeY()/2): #Le point (0,0) est au centre de l'écran donc normalement ça passe
                return distance

            #Detection des obstacles
            for l in self._terrain.getListeObstacles():
                if l.estDedans(posRayon[0], posRayon[1]):
                    return distance
            
            tickRayon = 0.1
            distance += tickRayon
            posRayon = (posRayon[0] + tickRayon * dirVect[0], posRayon[1] + tickRayon * dirVect[1])

    def actualiser(self, dT : float):
        """
        Actualise la simulation selon le temps dT écoulé depuis la dernière actualisation

        Paramètres:
        dT -> différence de temps (en seconde)
        """

        for robot in self._robotsList:
            print(robot.getInfo()+"\tDist: "+str(format(self.getDistanceFromRobot(robot),'.2f'))) 
            if (self.getDistanceFromRobot(robot) > 50):
                if(robot.getVitesseGauche() > robot.getVitesseDroite()):
                    robot.accelererDroite(7)
                elif(robot.getVitesseDroite() > robot.getVitesseGauche()):
                    robot.accelererGauche(7)
                else:
                    robot.accelerer(2)
            elif(self.getDistanceFromRobot(robot) > 20 and abs(robot.getVitesseGauche()) >0 and  abs(robot.getVitesseDroite()) > 0):
                robot.ralentirGauche(20)
            else:
                robot.accelererGauche(-50)
                robot.accelererDroite(-50)

            robot.actualiser(dT)

    

                       

