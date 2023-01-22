from Robot import Robot
from Terrain import Terrain

class Simulation : 
    """
    Classe représentant la simulation
    """

    def __init__(self, robotsList : list = None, terrain : Terrain = None):
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
    

    def ajouterRobot(self, robot : Robot):
        """
        Ajoute un robot dans la liste des robots de la simulation

        Paramètres:
        robot -> le robot à ajouter dans la liste
        """

        self._robotsList.append(robot)

    
    def retirerRobot(self, robot : Robot):
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

    def setTerrain(self, terrain : Terrain):
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
        