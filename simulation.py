import objets as o
from math import cos, sin, radians, degrees
import pygame

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

        self.lastPosX = 0
        self.lastPosY = 0
    

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
        if robot in self._robotsList:
            self._robotsList.remove(robot)


    def retirerRobotId(self, index : int):
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


    #Capteur de distance
    def getDistanceFromRobot(self, robot: o.Robot):
        """
        Renvoie la distance jusqu'au prochain obstacle
        
        Paramètres:
        terrain -> Terrain
        """
        dirVect = (cos(radians(robot.getAngle())), sin(radians(-robot.getAngle())))
        posRayon = (robot.getX(), robot.getY())
        distance = 0

        while distance < self._terrain.getSizeX() * self._terrain.getSizeY(): #Limite pour pas que le rayon n'avance à l'infini
            #Detection des obstacles
            for l in self._terrain.getListeObstacles():
                if l.estDedans(posRayon[0], posRayon[1]):
                    self.lastPosX = posRayon[0] #Retour X de la position de l'impact du rayon
                    self.lastPosY = posRayon[1] #Retour Y de la position de l'impact du rayon
                    return distance
            
            tickRayon = 0.1
            distance += tickRayon
            newPosRayon = (posRayon[0] + tickRayon * dirVect[0], posRayon[1] + tickRayon * dirVect[1])
            posRayon = newPosRayon

    def actualiser(self, dT : float):
        """
        Actualise la simulation selon le temps dT écoulé depuis la dernière actualisation

        Paramètres:
        dT -> différence de temps (en seconde)
        """

        #Test du crash
        robotsARetirer = []
        for robot in self._robotsList:
            for obstacle in self._terrain.getListeObstacles():
                if(obstacle.testCrash(robot)):
                    print("crash")
                    robotsARetirer.append(robot)

        for r in robotsARetirer:
            self.retirerRobot(r)


        #Comportement des robots
        for robot in self._robotsList:
            #print(robot.getInfo()+"\tDist: "+str(format(self.getDistanceFromRobot(robot, scr),'.2f'))) 

            if (self.getDistanceFromRobot(robot) > 100):
                if(robot.getVitesseGauche() > robot.getVitesseDroite()):
                    robot.accelererDroite(14)
                elif(robot.getVitesseDroite() > robot.getVitesseGauche()):
                    robot.accelererGauche(14)
                else:
                    robot.accelerer(7)
            else:
                if (robot.getVitesseGauche() + robot.getVitesseDroite())/2 > 30:
                    robot.ralentir(1000/(self.getDistanceFromRobot(robot)+1))
                else:
                    robot.accelererGauche(20)

            robot.actualiser(dT)
