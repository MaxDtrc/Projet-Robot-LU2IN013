from . import objets as o
from math import cos, sin, radians
import json
from threading import Thread
import time

class Simulation(Thread): 
    """
    Classe représentant la simulation
    """

    def __init__(self, dT: int, robotsList : list = None, terrain : o.Terrain = None):
        """
        Constructeur de la classe Simulation

        :param robotsList : Liste de robots
        :param terrain : Le terrain
        """
        super(Simulation, self).__init__()

        self._wait = dT
        if robotsList is None : 
            self._robotsList = []
        else:
            self._robotsList = robotsList
        self.terrain = terrain

        #Dernier point détecté par le capteur de distance et s'il a été appelé
        self.capteurDistanceAppele = False 
        self.lastPosX = 0
        self.lastPosY = 0

    def run(self):
        self.running = True
        while self.running:
            self._lastTime = time.time()
            time.sleep(self._wait)
            self._dT = time.time() - self._lastTime
            self.actualiser()            
            
    def stop(self):
        self.running = False

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
            self.terrain.retirerObstacle(robot.nom)


    def retirerRobotId(self, index : int):
        """
        Retire le robot à l'index passé en paramètre de la liste de robots de la simulation 

        :param index : l'index du robot à enlever
        """
        self._robotsList.pop(index)

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
        :returns : la distance jusqu'au prochain obstacle (en mm)
        """
        dirVect = (cos(robot.angle), sin(-robot.angle))
        posRayon = (robot.x + dirVect[0] * robot.rayon, robot.y + dirVect[1] * robot.rayon)
        distance = 0
        tickRayon = 0.2

        while distance < self.terrain.sizeX * self.terrain.sizeY: #Limite pour pas que le rayon n'avance à l'infini
            #Detection des obstacles
            for i in range(0, self.terrain.getNombreObstacles()):
                if self.terrain.getObstacle(i).nom != robot.nom and self.terrain.getObstacle(i).estDedans(posRayon[0], posRayon[1]):
                    #Enregistrement des dernières valeurs observées (utiles pour du débogage ou l'affichage du rayon par exemple)
                    self.capteurDistanceAppele = True
                    self.lastPosX = posRayon[0] #On enregistre la dernière position X du rayon
                    self.lastPosY = posRayon[1] #On enregistre la dernière position Y du rayon

                    return distance
            

            #On augmente la distance et on fait avancer le rayon
            distance += tickRayon
            newPosRayon = (posRayon[0] + tickRayon * dirVect[0], posRayon[1] + tickRayon * dirVect[1])
            posRayon = newPosRayon

    def actualiser(self):
        """
        Actualise la simulation selon le temps dT écoulé depuis la dernière actualisation

        :param dT : différence de temps (en seconde)
        """

        #Update des robots
        for r in self._robotsList:
            r.actualiser(self._dT)

        #Test du crash
        robotsARetirer = []
        for robot in self._robotsList:
            for i in range(0, self.terrain.getNombreObstacles()):
                if(self.terrain.getObstacle(i).testCrash(robot)):
                    #Ajout du robot à la liste de ceux à retirer
                    robotsARetirer.append(robot)

        #Suppression des robots qui se sont crashés
        for r in robotsARetirer:
            self.retirerRobot(r)
    

        

def chargerJson(fichier : str, dT: int):
    """
    Crée les objets à partir d'un fichier json passé en paramètre

    :param fichier : le fichier json à charger
    :param dT : précision temporelle des robots
    """

    simulation = Simulation(dT)
        
    with open(fichier) as json_file:
        data = json.load(json_file)
        
        #Importation et initialisation du terrain
        t = data['terrain'] 
        simulation.terrain = o.Terrain(t['tailleX'], t['tailleY'])

        #Importation et initialisation des obstacles ronds
        for oR in data['obstaclesRonds'] :
            ob = o.ObstacleRond(oR['nom'], oR['posX'], oR['posY'], oR['rayon'])
            simulation.terrain.ajouterObstacle(ob)

        #Importation et initialisation des obstacles rectangles
        for oRect in data['obstaclesRectangles'] :
            ob = o.ObstacleRectangle(oRect['nom'], oRect['posX'], oRect['posY'], oRect['longueur'], oRect['largeur'])
            simulation.terrain.ajouterObstacle(ob)

        #Importation et initialisation des robots
        for rob in data['robots'] :
            r = o.Robot(rob['nom'], rob['posX'], rob['posY'], rob['angle'], rob['diametreRoues'], rob['rayon'], rob['vitesseGauche'], rob['vitesseDroite'], rob['vitesseMax'])
            simulation.ajouterRobot(r)
            simulation.terrain.ajouterObstacle(r)
        
    return simulation

def enregistrerJson(fichier:str, simulation):
    """
    Crée un fichier où sont enregistrées les données de la simulation

    :param fichier : le nom du fichier dans lequel écrire les données
    :param simulation : la simulation à enregistrer
    """
    d = dict()
    d["terrain"] = dict()
    d["terrain"]["tailleX"] = simulation.terrain.sizeX
    d["terrain"]["tailleY"] = simulation.terrain.sizeY

    d["obstaclesRonds"] =[]
    d["obstaclesRectangles"] =[]
    for i in range (0, simulation.terrain.getNombreObstacles()):
        obsdic = dict()
        o = simulation.terrain.getObstacle(i)
        if (o.type == 1) :
            obsdic["nom"] = o.nom
            obsdic["posX"] = o.x
            obsdic["posY"] = o.y
            obsdic["rayon"] = o.rayon
            d["obstaclesRonds"].append(obsdic)
        elif (o.type == 0) :
            obsdic["nom"] = o.nom
            obsdic["posX"] = o.x
            obsdic["posY"] = o.y
            obsdic["longueur"] = o.longueur
            obsdic["largeur"] = o.largeur
            d["obstaclesRectangles"].append(obsdic)

    d["robots"] = []

    for i in range(0, simulation.getNombreDeRobots()):
        robdic = dict()
        r = simulation.getRobot(i)
        robdic["nom"] = r.nom
        robdic["posX"] = r.x
        robdic["posY"] = r.y
        robdic["angle"] = r.angle
        robdic["diametreRoues"] = r.tailleRoues
        robdic["rayon"] = r.rayon
        robdic["vitesseGauche"] = r.vitesseGauche
        robdic["vitesseDroite"] = r.vitesseDroite
        robdic["vitesseMax"] = r.vitesseMax
        d["robots"].append(robdic)
   
    with open(fichier, "w") as json_file:
        json_file.write(json.dumps(d, indent=4))
