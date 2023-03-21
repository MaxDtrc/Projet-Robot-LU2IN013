import pygame
from math import cos, sin, degrees
import os
from threading import Thread, enumerate
import time
import sys
import keyboard

from math import pi, sin, cos

#Panda3d
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from direct.gui.OnscreenText import OnscreenText

from panda3d.core import Point3, Filename

from panda3d.core import loadPrcFileData, OrthographicLens, TextureStage, PointLight

loadPrcFileData("", "win-size 720 720")

from .. import simulation as s

#Initialisation de variables globales
COULEUR_OBSTACLES = (65, 0, 55)
COULEUR_ROBOT = (255, 165, 165)
BLACK = (0, 0, 0)

path = Filename.fromOsSpecific(os.path.dirname(os.path.realpath(__file__))).getFullpath()




class Affichage(Thread):
    def __init__(self, simulation : s.Simulation, controleur, fps: int, echelle: int = 1, afficherDistance: bool = False, afficherTrace: bool = False):
        """
        Constructeur de la classe affichage
        
        :param simulation : Simulation concernée par cet affichage
        :param controleur : Controleur concernée par cet affichage
        :param fps : Le nombre d'fps de la simulation
        :param echelle : Echelle de la simulation
        :param afficherDistance : Booleen pour afficher la distance entre le robot et les obstacles
        :param afficherTrace : Booleen pour choisir si le robot laisse une trace sur son passage
        """
        super(Affichage, self).__init__()
        self._simulation = simulation
        self._controleur = controleur
        self._fps = fps
        self._echelle = echelle
        self._afficherDistance = afficherDistance
        self._afficherTrace = afficherTrace
        self.tailleTrace = 2

        #Init de pygame
        pygame.init()
        self._trace = pygame.surface.Surface((simulation.terrain.sizeX * self._echelle, simulation.terrain.sizeY * self._echelle))
        self._screen = pygame.display.set_mode((simulation.terrain.sizeX * self._echelle, simulation.terrain.sizeY * self._echelle))
        pygame.display.set_caption('Test de la simulation du robot') 
        self._screen.fill((255,255,255))
        self._trace.fill((255, 255, 255))
        

    def run(self):
        self.running = True
        while self.running:
            self.afficherSimulation()
            time.sleep(1./self._fps)

    def stop(self):
        self.running = False

    def _afficherObstacle(self, obstacle : s.Obstacle):
        """
        Affiche un obstacle sur la fenêtre
        
        :param obstacle : Obstacle à afficher
        """
        e = self._echelle
        if (obstacle.type == 0):
            #Affichage d'un obstacle rectangle
            pygame.draw.rect(self._screen, COULEUR_OBSTACLES, (obstacle.x*e + self._screen.get_size()[0]/2 - obstacle.longueur*e/2, obstacle.y*e + self._screen.get_size()[1]/2 - obstacle.largeur*e/2, obstacle.longueur*e, obstacle.largeur*e))
        elif (obstacle.type == 1):
            #Affichage d'un obstacle rond
            pygame.draw.circle(self._trace, COULEUR_OBSTACLES, (obstacle.x*e + self._screen.get_size()[0]/2, obstacle.y*e + self._screen.get_size()[0]/2), obstacle.rayon*e)

    def _afficherRobot(self, robot: s.Robot):
        """
        Affiche un robot sur la fenêtre
        
        :param robot : Robot à afficher
        """
        e = self._echelle
        #Image de base
        image_pas_tournee = pygame.image.load(os.path.dirname(os.path.realpath(__file__)) + "/robot.png").convert_alpha()
        image_pas_tournee = pygame.transform.scale(image_pas_tournee, (image_pas_tournee.get_width()/15 * robot.rayon *e, image_pas_tournee.get_height()/15 * robot.rayon *e))
        
        #Image que l'on tourne en fonction de l'angle du robot
        image = pygame.transform.rotate(image_pas_tournee, degrees(robot.angle))

        #Affichage du robot sur le self._screen
        pygame.draw.circle(self._screen, COULEUR_ROBOT, (robot.x*e + self._screen.get_size()[0]/2, robot.y*e + self._screen.get_size()[0]/2), robot.rayon*e)
        self._screen.blit(image, (self._screen.get_size()[0]/2 - image.get_width()/2 + robot.x*e, self._screen.get_size()[1]/2 - image.get_height()/2 + robot.y*e))

        if self._afficherTrace:
            #affichage du tracé du robot sur la surface
            pygame.draw.circle(self._trace, BLACK, (robot.x*e + self._trace.get_size()[0]/2, robot.y*e + self._trace.get_size()[0]/2), self.tailleTrace)


    def afficherSimulation(self):
        """
        Affiche l'ensemble de la simulation sur la fenêtre
        
        """
        e = self._echelle

        #Fill de l'écran
        #self._screen.fill((255,255,255))

        #Affichage du tracé
        self._screen.blit(self._trace, (0, 0))
        
        #Affichage des objets
        t = self._simulation.terrain
        for i in range(0, self._simulation.getNombreDeRobots()):
            r = self._simulation.getRobot(i)
            self._afficherRobot(r)

            #Affichage du capteur de distance
            if self._afficherDistance and self._simulation.capteurDistanceAppele:
                pygame.draw.line(self._screen, (255, 0, 0), ((r.x + cos(r.angle) * r.rayon)*e + t.sizeX*e/2, (r.y + sin(-r.angle) * r.rayon)*e + t.sizeY*e/2), (self._simulation.lastPosX*e  + t.sizeX*e/2, self._simulation.lastPosY*e  + t.sizeY*e/2))
                self._simulation.capteurDistanceAppele = False
        for i in range(0, t.getNombreObstacles()):
            self._afficherObstacle(t.getObstacle(i))

        #Actualisation de l'écran
        pygame.display.update()
        
        #Fermeture de la fenêtre
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                self._simulation.stop() #On arrête la simulation
                self._controleur.stop_ia_thread() #On arrête l'ia
                self.stop() #On arrête l'affichage
                exit() #On arrête.


class Affichage3d(Thread):
    def __init__(self, simulation : s.Simulation, controleur, fps: int):
        """
        Constructeur de la classe affichage
        
        :param simulation : Simulation concernée par cet affichage
        :param controleur : Controleur concernée par cet affichage
        :param fps : Le nombre d'fps de la simulation
        """
        super(Affichage3d, self).__init__()
        self._simulation = simulation
        self._controleur = controleur
        self._fps = fps
        self.pov = True

        self.app = MyApp()

        #Ajout de la lumière
        plight = PointLight('plight')
        plight.setShadowCaster(True, 256, 256)
        self.app.render.setShaderAuto()
        plight.setColor((1, 1, 1, 1))
        plnp = self.app.render.attachNewNode(plight)
        plnp.setPos(0, 50, 100)
        self.app.render.setLight(plnp)

        #Ajout d'un texte pour les touches
        textObject = OnscreenText(text='Appuyer sur q pour changer de POV', pos=(0.6, 0.9), scale=0.04, fg=(255,255,255,1), shadow = (0,0,0,1))

        #Affichage des murs
        mdl = self.app.loader.loadModel(path + "/models/cube/cube.obj")
        mdl.setPos(0, 0, -2)
        mdl.setScale(self._simulation.terrain.sizeX/2, self._simulation.terrain.sizeY/2, 2)

        mdl.reparentTo(self.app.render)

        #Affichage du sol

        ts = TextureStage('ts')
        txt = self.app.loader.loadTexture(path + "/models/cube/WoodFloor040_1K_Color_1.png")
        mdl.setTexture(ts, txt)
        mdl.setTexScale(ts, 10, 10)

        self.app.obsList.append(mdl)

        self._afficherObstacles()

    def run(self):
        self.app.running = True
        while self.app.running:
            self.afficherSimulation()
            time.sleep(1./self._fps)
        self.stop()

    def stop(self):
        self._simulation.stop() #On arrête la simulation
        self._controleur.stop_ia_thread() #On arrête l'ia

        self.app.destroy() #on arrête l'app

        return #on arrête

    def _afficherObstacles(self):
        """
        Affiche un obstacle sur la fenêtre
        
        """
        #Affichage des obstacles
        for i in range(self._simulation.terrain.getNombreObstacles()):
            o = self._simulation.terrain.getObstacle(i)

            mdl = self.app.loader.loadModel(path + "/models/cube/cube.obj")
            mdl.setPos(o._posX, o._posY, 0)
            mdl.setScale(o._longueur/2, o._largeur/2, 10)
            mdl.reparentTo(self.app.render)

            self.app.obsList.append(mdl)

    def _afficherRobot(self, robot: s.Robot):
        """
        Affiche un robot sur la fenêtre
        
        :param robot : Robot à afficher
        """

        self.app.robotModel.setPos(robot.x, -robot.y, 0)
        self.app.robotModel.setHpr(degrees(robot.angle) + 90, 90, 0)

        #Changement de pov en appuyant sur q
        if keyboard.is_pressed('q'):
            while keyboard.is_pressed('q'):
                pass
            self.pov = not self.pov

        if self.pov:
            self.app.camera.setPos(robot.x, -robot.y, 4.5)
            self.app.camera.setHpr(degrees(robot.angle) - 90, 0, 0)
        else:
            self.app.camera.setPos(0, 0, 350)
            self.app.camera.setHpr(0, -90, 0)

    def afficherSimulation(self):
        """
        Affiche l'ensemble de la simulation sur la fenêtre
        
        """
        #Affichage des objets
        t = self._simulation.terrain
        for i in range(0, self._simulation.getNombreDeRobots()):
            r = self._simulation.getRobot(i)
            self._afficherRobot(r)

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.robotModel = Actor(path + "/models/Blazing_Banana/banana.obj" )
        self.robotModel.setScale(2, 2, 2)
        self.robotModel.reparentTo(self.render)

        self.obsList = list()

        self.robotModel.loop("walk")

    def spinCameraTask(self, task):
        return Task.cont
    
    def userExit(self):
        self.running = False
        self.shutdown()