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

        #Dernier point détecté par le capteur de distance et s'il a été appelé (pour chaque robot)
        self.capteurDistanceAppele = {k:False for k in [r.nom for r in self._robotsList]}
        self.lastPosRayon = {k:(0, 0) for k in [r.nom for r in self._robotsList]}


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
        self.capteurDistanceAppele[robot.nom] = False
        self.lastPosRayon[robot.nom] = (0, 0)

    
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
        dirVect = (cos(robot._angle + radians(robot._angleCamera - 90)), sin(-robot._angle + radians(robot._angleCamera - 90)))
        posRayon = (robot.x + dirVect[0] * robot.rayon, robot.y + dirVect[1] * robot.rayon)
        distance = 0
        tickRayon = 0.2

        while distance < self.terrain.sizeX * self.terrain.sizeY: #Limite pour pas que le rayon n'avance à l'infini
            #Detection des obstacles
            for i in range(0, self.terrain.getNombreObstacles()):
                if self.terrain.getObstacle(i).nom != robot.nom and self.terrain.getObstacle(i).estDedans(posRayon[0], posRayon[1]):
                    #Enregistrement des dernières valeurs observées (utiles pour du débogage ou l'affichage du rayon par exemple)
                    self.capteurDistanceAppele[robot.nom] = True
                    self.lastPosRayon[robot.nom] = (posRayon[0], posRayon[1]) #On enregistre la dernière position du rayon

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
            self.terrain.retirerObstacle(robot)
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

        #Importation et initialisation des balises
        for balise in data['balises'] :
            ob = o.Balise(balise['nom'], balise['type_balise'], balise['posX'], balise['posY'], balise['angle'])
            simulation.terrain.ajouterObstacle(ob)

        #Importation et initialisation des robots
        for rob in data['robots'] :
            r = o.Robot(rob['nom'], rob['posX'], rob['posY'], rob['angle'], 6.65, 5.85, 0, 0, 10000)
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
    d["terrain"] = {"tailleX": simulation.terrain.sizeX, "tailleY": simulation.terrain.sizeY}

    d["obstaclesRonds"] =[]
    d["obstaclesRectangles"] =[]
    d["balises"] =[]
    for i in range (0, simulation.terrain.getNombreObstacles()):
        obsdic = dict()
        o = simulation.terrain.getObstacle(i)
        if (o.type == 1) :
            obsdic = {"nom": o.nom, "posX": o.x, "posY": o.y, "rayon": o.rayon}
            d["obstaclesRonds"].append(obsdic)
        elif (o.type == 0) :
            obsdic = {"nom": o.nom, "posX": o.x, "posY": o.y, "longueur": o.longueur, "largeur": o.largeur}
            d["obstaclesRectangles"].append(obsdic)
        elif (o.type == 2) :
            obsdic = {"nom": o.nom, "posX": o.x, "posY": o.y, "angle": o.angle, "type_balise": o.type_balise}
            d["balises"].append(obsdic)

    d["robots"] = []
    for i in range(0, simulation.getNombreDeRobots()):
        robdic = dict()
        r = simulation.getRobot(i)

        robdic = {"nom": r.nom, "posX": r.y, "posY": r.y, "angle": r.angle}
        d["robots"].append(robdic)
   
    with open(fichier, "w") as json_file:
        json_file.write(json.dumps(d, indent=4))
