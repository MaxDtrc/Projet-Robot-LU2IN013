from robot.simulation.objets import Robot, Obstacle, ObstacleRectangle, ObstacleRond, Terrain
from robot.simulation.simulation import Simulation
import unittest

class TestSimulation(unittest.TestCase):
    
    def setUp(self):
        terrain = Terrain(10,10)
        robot1 = Robot("Andrew", 0, 0, 0, 5, 10, 200)
        liste_robot=[robot1]
        self.s = Simulation(10,liste_robot,terrain)

    def TestGetNombreDeRobots(self):
        self.assertEqual(self.s.getNombreDeRobots(),1)

    def TestAjouterRobot(self):
        robot2 = Robot("Tristan", 5, 5, 0, 5, 10, 200)
        self.s.ajouterRobot(robot2)
        self.assertEqual(self.s.getNombreDeRobots(),2)

    def TestGetRobot(self):
        robot1 = Robot("Andrew", 0, 0, 0, 5, 10, 200)
        self.assertEqual(self.s.getRobot(1),robot1)

    def TestRetirerRobotId(self):
        self.s.retirerRobotId(1)
        robot2 = Robot("Tristan", 5, 5, 0, 5, 10, 200)
        self.assertEqual(self.s.getNombreDeRobots(),1)
        self.assertEqual(self.s.getRobot(1),robot2)

    


