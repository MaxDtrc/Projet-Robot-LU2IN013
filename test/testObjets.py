from math import cos, sin, radians, degrees, sqrt
from robot import Robot, Obstacle, ObstacleRectangle, ObstacleRond
import unittest

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.r = Robot("MJ", 20, 45, 0, 10, 200)

    def testNom(self):
        self.assertEqual(self.r.getNom(), "MJ")

    def testGetX(self):
        self.assertEqual(self.r.getX(), 20)

    def testGetY(self):
        self.assertEqual(self.r.getY(), 45)

    def testGetPosition(self):
        self.assertEqual(self.r.getPosition(), (20,45))

    def testGetAngle(self):
        self.assertEqual(self.r.getAngle(), 0)

    def testGetRayon(self):
        self.assertEqual(self.r.getRayon(), 10)

    def testGetPosRoueGaucheX(self):
        self.assertEqual(self.r.getPosRoueGaucheX(), 20)

    def testGetPosRoueGaucheY(self):
        self.assertEqual(self.r.getPosRoueGaucheY(), 55)

    def testGetPosRoueDroiteX(self):
        self.assertEqual(self.r.getPosRoueDroiteX(), 20)

    def testGetPosRoueDroiteY(self):
        self.assertEqual(self.r.getPosRoueDroiteY(), 35)

    def testGetPosRoueGauche(self):
        self.assertEqual(self.r.getPosRoueGauche(),(20,55))

    def testGetPosRoueDroite(self):
        self.assertEqual(self.r.getPosRoueDroite(),(20,35))
    
    def testGetVitesseDroite(self):
        self.assertEqual(self.r.getVitesseDroite(), 0)

    def testGetVitesseGauche(self):
        self.assertEqual(self.r.getVitesseGauche(), 0)
       
    def testGetInfo(self):
        self.assertEqual(self.r.getInfo(),"VitG: 0.00\tVitD: 0.00\tAngle: 0.00")
    
    def testSetVitesseDroite(self):
        self.r.setVitesseDroite(250)
        self.assertEqual(self.r.getVitesseDroite(), 200)
        self.r.setVitesseDroite(50)
        self.assertEqual(self.r.getVitesseDroite(), 50)
        self.r.setVitesseDroite(-50)
        self.assertEqual(self.r.getVitesseDroite(), -50)
        self.r.setVitesseDroite(-250)
        self.assertEqual(self.r.getVitesseDroite(), -200)

    def testSetVitesseGauche(self):
        self.r.setVitesseGauche(250)
        self.assertEqual(self.r.getVitesseGauche(), 200)
        self.r.setVitesseGauche(50)
        self.assertEqual(self.r.getVitesseGauche(), 50)
        self.r.setVitesseGauche(-50)
        self.assertEqual(self.r.getVitesseGauche(), -50)
        self.r.setVitesseGauche(-250)
        self.assertEqual(self.r.getVitesseGauche(), -200)

    def testSetVitesse(self):
        self.r.setVitesse(250)
        self.assertEqual(self.r.getVitesse(), (200,200))
        self.r.setVitesse(50)
        self.assertEqual(self.r.getVitesse(), (50,50))
        self.r.setVitesse(-50)
        self.assertEqual(self.r.getVitesse(), (-50,-50))
        self.r.setVitesse(-250)
        self.assertEqual(self.r.getVitesse(), (-200,-200))

    def testActualiser(self):
        self.r.setVitesse(20)
        self.r.actualiser(0.1)
        self.assertEqual(self.r.getPosition(), (22,45))
        self.assertEqual(self.r.getAngle(), 0)
        self.r.actualiser(0.1)
        self.assertEqual(self.r.getPosition(), (24,45))
        self.assertEqual(self.r.getAngle(), 0)
        self.r.setVitesseDroite(10)
        self.r.setVitesseGauche(30)
        self.r.actualiser(0.1)
        self.assertEqual(self.r.getPosition(), (26,45))
        self.assertEqual(self.r.getAngle(), degrees(-0.2)%360)
        self.r.actualiser(0.1)
        self.assertEqual(self.r.getPosition(), (26+(2*cos(radians(degrees(-0.2)%360))),45-(2*sin(radians(degrees(-0.2)%360)))))
        self.assertEqual(self.r.getAngle(), degrees(radians(degrees(-0.2)%360)-0.2)%360)
        
class TestObstacleRond(unittest.TestCase):
    def setUp(self):
        self.obs = ObstacleRond("ObsOne", 100, 80, 10)

    def testGetNom(self):
        self.assertEqual(self.obs.getNom(), "ObsOne")

    def testGetPosition(self):
        self.assertEqual(self.obs.getPosition(), (100,80))
    
    def testGetX(self):
        self.assertEqual(self.obs.getX(), 100)

    def testGetY(self):
        self.assertEqual(self.obs.getY(), 80)

    def testGetRayon(self):
        self.assertEqual(self.obs.getRayon(), 10)
    
    def testSetPosition(self):
        self.obs.setPosition(-100, -80)
        self.assertEqual(self.obs.getPosition(), (-100, -80))

    def testEstDedans(self):
        self.assertTrue(self.obs.estDedans(95,75))
        self.assertFalse(self.obs.estDedans(30,50))

    def testTestCrash(self):
        r = Robot("Driftator", 95, 75, 0, 15, 200)
        self.assertEqual(self.obs.testCrash(r), 1)
        r1 = Robot("Driftator", 100, 80, 0, 15, 200)
        self.assertEqual(self.obs.testCrash(r1), 1)
        r2 = Robot("Driftator", 30, 50, 0, 15, 200)
        self.assertEqual(self.obs.testCrash(r2), 0)

class TestObstacleRectangle(unittest.TestCase):
    def setUp(self):
        self.obr = ObstacleRectangle("ObsRec", 100, 80, 10,20)

    def testGetNom(self):
        self.assertEqual(self.obr.getNom(), "ObsRec")

    def testGetPosition(self):
        self.assertEqual(self.obr.getPosition(), (100,80))
    
    def testGetX(self):
        self.assertEqual(self.obr.getX(), 100)

    def testGetY(self):
        self.assertEqual(self.obr.getY(), 80)

    def testGetLongueur(self):
        self.assertEqual(self.obr.getLongueur(), 10)

    def testGetLargeur(self):
        self.assertEqual(self.obr.getLargeur(), 20)
    
    def testSetPosition(self):
        self.obr.setPosition(-100, -80)
        self.assertEqual(self.obr.getPosition(), (-100, -80))

    def testEstDedans(self):
        self.assertTrue(self.obr.estDedans(95,75))
        self.assertFalse(self.obr.estDedans(30,50))

    def testTestCrash(self):
        r = Robot("Driftator", 95, 75, 0, 15, 200)
        self.assertEqual(self.obr.testCrash(r), 1)
        r1 = Robot("Driftator", 100, 80, 0, 15, 200)
        self.assertEqual(self.obr.testCrash(r1), 1)
        r2 = Robot("Driftator", 30, 50, 0, 15, 200)
        self.assertEqual(self.obr.testCrash(r2), 0)

if __name__ == "__main__":
    unittest.main()
