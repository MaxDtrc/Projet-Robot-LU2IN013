from .. import objets as o
from math import cos, sin, radians, degrees
import pygame
import json

class Simulation : 
    """
    Classe représentant la simulation
    """

    def __init__(self, robotsList : list = None, terrain : o.Terrain = None):
        """
        Constructeur de la classe Simulation

        :param robotsList : Liste de robots
        :param terrain : Le terrain
        """
        
        if robotsList is None : 
            self._robotsList = []
        else:
            self._robotsList = robotsList
        self._terrain = terrain

        self.lastPosX = 0
        self.lastPosY = 0
    
    def chargerJson(self, fichier : str):
        """
        Crée les objets à partir d'un fichier json passé en paramètre

        :param fichier : le fichier json à charger
        """
        with open(fichier) as json_file:
            data = json.load(json_file)
        
            #Importation et initialisation du terrain
            t = data['terrain'] 
            self._terrain = o.Terrain(t['tailleX'], t['tailleY'])

            #Importation et initialisation des obstacles ronds
            for oR in data['obstaclesRonds'] :
                ob = o.ObstacleRond(oR['nom'], oR['posX'], oR['posY'], oR['rayon'])
                self._terrain.ajouterObstacle(ob)

            #Importation et initialisation des obstacles rectangles
            for oRect in data['obstaclesRectangles'] :
                ob = o.ObstacleRectangle(oRect['nom'], oRect['posX'], oRect['posY'], oRect['longueur'], oRect['largeur'])
                self._terrain.ajouterObstacle(ob)

            #Importation et initialisation des robots
            for rob in data['robots'] :
                r = o.Robot(rob['nom'], rob['posX'], rob['posY'], rob['angle'], rob['tailleRoues'], rob['rayon'], rob['vitesseMax'])
                self.ajouterRobot(r)

    def ajouterRobot(self, robot : o.Robot):
        """
        Ajoute un robot dans la liste des robots de la simulation

        :param robot : le robot à ajouter dans la liste
        """

        self._robotsList.append(robot)

    
    def retirerRobot(self, robot : o.Robot):
        """
        Retire le robot passé en paramètre de la liste des robots de la simulation

        :param robot : le robot à retirer de la liste
        """
        if robot in self._robotsList:
            self._robotsList.remove(robot)


    def retirerRobotId(self, index : int):
        """
        Retire le robot à l'index passé en paramètre de la liste de robots de la simulation 

        :param index : l'index du robot à enlever
        """
        self._robotsList.pop(index)

    @property
    def terrain(self):
        """
        :returns : le Terrain affecté à la variable Terrain de la simulation
        """
        return self._terrain

    @terrain.setter
    def terrain(self, terrain : o.Terrain):
        """
        Affecte le terrain passé en paramètre à la variable Terrain de la simulation

        :param terrain : le terrain à affecter
        """
        self._terrain = terrain

    def getNombreDeRobots(self):
        """
        :returns : le nombre de robots présents dans la simulation
        """
        return len(self._robotsList)
        
    def getRobot(self, index : int):
        """
        :param index : l'index du robot à renvoyer
        :returns : le robot correspondant à l'index passé en paramètre dans le tableau de robots
        """
        return self._robotsList[index]


    #Capteur de distance
    def getDistanceFromRobot(self, robot: o.Robot):
        """ 
        :param terrain : Terrain
        :returns : la distance jusqu'au prochain obstacle
        """
        dirVect = (cos(radians(robot.angle)), sin(radians(-robot.angle)))
        posRayon = (robot.x + dirVect[0], robot.y + dirVect[1])
        distance = 0

        while distance < self._terrain.sizeX * self._terrain.sizeY: #Limite pour pas que le rayon n'avance à l'infini
            #Detection des obstacles
            for i in range(0, self._terrain.getNombreObstacles()):
                if self._terrain.getObstacle(i).estDedans(posRayon[0], posRayon[1]):
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

        :param dT : différence de temps (en seconde)
        """

        #Test du crash
        robotsARetirer = []
        for robot in self._robotsList:
            for i in range(0, self._terrain.getNombreObstacles()):
                if(self._terrain.getObstacle(i).testCrash(robot)):
                    robotsARetirer.append(robot)

        for r in robotsARetirer:
            self.retirerRobot(r)


        #Comportement des robots
        for robot in self._robotsList:
            if (self.getDistanceFromRobot(robot) > 100):
                if(robot.vitesseGauche > robot.vitesseDroite):
                    robot.vitesseDroite += 14
                elif(robot.vitesseDroite > robot.vitesseGauche):
                    robot.vitesseGauche += 14
                else:
                    robot.vitesse = robot.vitesseGauche + 7
            else:
                if (robot.vitesseGauche + robot.vitesseDroite)/2 > 30:
                    robot.vitesse = robot.vitesseGauche - 1000/(self.getDistanceFromRobot(robot)+1)
                else:
                    robot.vitesseGauche += 20

            robot.actualiser(dT)
