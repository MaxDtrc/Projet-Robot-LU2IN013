import driftator.simulation
import unittest

class TestSimulation(unittest.TestCase):
    def setUp(self):
        terrain = driftator.simulation.Terrain(10,10)
        robot1 = driftator.simulation.Robot("Andrew", 0, 0, 0, 5, 10, 200)
        liste_robot=[robot1]
        self.s = driftator.simulation.Simulation(1,liste_robot,terrain)
        #La simulation contient 1 robot "Andrew"

    def testGetNombreDeRobots(self):
        self.assertEqual(self.s.getNombreDeRobots(),1)

    def testAjouterRobot(self):
        robot2 = driftator.simulation.Robot("Tristan", 5, 5, 0, 5, 10, 200)
        self.s.ajouterRobot(robot2)
        self.assertEqual(self.s.getNombreDeRobots(),2)

    def testRetirerRobot(self):
        robot1 = driftator.simulation.Robot("Andrew", 0, 0, 0, 5, 10, 200)
        self.s.ajouterRobot(robot1)
        self.s.retirerRobot(robot1)
        self.assertEqual(self.s.getNombreDeRobots(),1)
        
    def testGetRobot(self):
        robot1 = driftator.simulation.Robot("Andrew", 0, 0, 0, 5, 10, 200)
        self.s.ajouterRobot(robot1)
        self.assertEqual(self.s.getRobot(1),robot1)

    def testRetirerRobotId(self):
        self.s.retirerRobotId(0)
        self.assertEqual(self.s.getNombreDeRobots(),0)

if __name__ == "__main__":
    unittest.main()
