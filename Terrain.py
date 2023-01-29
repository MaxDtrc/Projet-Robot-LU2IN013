from Obstacle import Obstacle

class Terrain:
    """
    Classe représentant un terrain
    """

    def __init__(self, sizeX: int, sizeY: int):
        """
        Constructeur de la classe
        
        Paramètres:
        sizeX -> taille X du terrain
        sizeY -> taille Y du terrain
        """
        self._sizeX = sizeX
        self._sizeY = sizeY
        self._listeObstacles = list()
    
    def getSize(self):
        """
        Renvoie un tuple correspondant à la taille du terrain (sizeX, sizeY)
        """
        return (self._sizeX, self._sizeY)

    def getSizeX(self):
        """
        Renvoie la taille X du terrain
        """
        return self._sizeX

    def getSizeY(self):
        """
        Renvoie la taille Y du terrain
        """
        return self._sizeY

    def addObstacle(self, obstacle : Obstacle):
        """
        Ajoute un obstacle à la liste des obstacles du terrain
        """

        self._listeObstacles.append(obstacle)

    def getListeObstacles(self):
        """
        Renvoie la liste des obstacles du terrain
        """
        return self._listeObstacles