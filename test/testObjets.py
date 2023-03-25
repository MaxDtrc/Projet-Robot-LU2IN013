from math import cos, sin, radians, degrees, sqrt
import driftator_sim as driftator
import unittest

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.r = driftator.simulation.Robot("MJ", 20, 45, 0, 5, 10, 200, 0, 200)

    def testNom(self):
        self.assertEqual(self.r.nom, "MJ")

    def testGetX(self):
        self.assertEqual(self.r.x, 20)

    def testGetY(self):
        self.assertEqual(self.r.y, 45)

    def testGetPosition(self):
        self.assertEqual(self.r.position, (20,45))

    def testGetAngle(self):
        self.assertEqual(self.r.angle, 0)

    def testGetRayon(self):
        self.assertEqual(self.r.rayon, 10)

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
        self.assertEqual(self.r.vitesseDroite, 0)

    def testGetVitesseGauche(self):
        self.assertEqual(self.r.vitesseGauche, 200)
       
    def testGetInfo(self):
        self.assertEqual(self.r.getInfo(),"VitG: 200.00\tVitD: 0.00\tAngle: 0.00")
    
    def testSetVitesseDroite(self):
        self.r.vitesseDroite = 250
        self.assertEqual(self.r.vitesseDroite, 200)
        self.r.vitesseDroite = 50
        self.assertEqual(self.r.vitesseDroite, 50)
        self.r.vitesseDroite = -50
        self.assertEqual(self.r.vitesseDroite, -50)
        self.r.vitesseDroite = -250
        self.assertEqual(self.r.vitesseDroite, -200)

    def testSetVitesseGauche(self):
        self.r.vitesseGauche = 250
        self.assertEqual(self.r.vitesseGauche, 200)
        self.r.vitesseGauche = 50
        self.assertEqual(self.r.vitesseGauche, 50)
        self.r.vitesseGauche = -50
        self.assertEqual(self.r.vitesseGauche, -50)
        self.r.vitesseGauche = -250
        self.assertEqual(self.r.vitesseGauche, -200)

    def testSetVitesse(self):
        self.r.vitesse = 250
        self.assertEqual(self.r.vitesse, (200,200))
        self.r.vitesse = 50
        self.assertEqual(self.r.vitesse, (50,50))
        self.r.vitesse = -50
        self.assertEqual(self.r.vitesse, (-50,-50))
        self.r.vitesse = -250
        self.assertEqual(self.r.vitesse, (-200,-200))

    def testActualiser(self):
        self.r.vitesse = 180
        self.r.actualiser(0.1)
        self.assertAlmostEqual(self.r.position[0], 20.785, 3)
        self.assertEqual(self.r.angle, 0)
        self.r.actualiser(0.1)
        self.assertAlmostEqual(self.r.position[0], 21.57, 2)
        self.assertEqual(self.r.angle, 0)

        
class TestObstacleRond(unittest.TestCase):
    def setUp(self):
        self.obs = driftator.simulation.ObstacleRond("ObsOne", 100, 80, 10)

    def testGetNom(self):
        self.assertEqual(self.obs.nom, "ObsOne")

    def testGetPosition(self):
        self.assertEqual(self.obs.getPosition(), (100,80))
    
    def testGetX(self):
        self.assertEqual(self.obs.x, 100)

    def testGetY(self):
        self.assertEqual(self.obs.y, 80)

    def testGetRayon(self):
        self.assertEqual(self.obs.rayon, 10)
    
    def testSetPosition(self):
        self.obs.setPosition(-100, -80)
        self.assertEqual(self.obs.getPosition(), (-100, -80))

    def testEstDedans(self):
        self.assertTrue(self.obs.estDedans(95,75))
        self.assertFalse(self.obs.estDedans(30,50))

    def testTestCrash(self):
        r = driftator.simulation.Robot("Driftator", 95, 75, 0, 5, 15, 200)
        self.assertEqual(self.obs.testCrash(r), 1)
        r1 = driftator.simulation.Robot("Driftator", 100, 80, 0, 5, 15, 200)
        self.assertEqual(self.obs.testCrash(r1), 1)
        r2 = driftator.simulation.Robot("Driftator", 30, 50, 0, 5, 15, 200)
        self.assertEqual(self.obs.testCrash(r2), 0)

class TestObstacleRectangle(unittest.TestCase):
    def setUp(self):
        self.obr = driftator.simulation.ObstacleRectangle("ObsRec", 100, 80, 10,20)

    def testGetNom(self):
        self.assertEqual(self.obr.nom, "ObsRec")

    def testGetPosition(self):
        self.assertEqual(self.obr.getPosition(), (100,80))
    
    def testGetX(self):
        self.assertEqual(self.obr.x, 100)

    def testGetY(self):
        self.assertEqual(self.obr.y, 80)

    def testGetLongueur(self):
        self.assertEqual(self.obr.longueur, 10)

    def testGetLargeur(self):
        self.assertEqual(self.obr.largeur, 20)
    
    def testSetPosition(self):
        self.obr.setPosition(-100, -80)
        self.assertEqual(self.obr.getPosition(), (-100, -80))

    def testEstDedans(self):
        self.assertTrue(self.obr.estDedans(95,75))
        self.assertFalse(self.obr.estDedans(30,50))

    def testTestCrash(self):
        r = driftator.simulation.Robot("Driftator", 95, 75, 0, 5, 15, 200)
        self.assertEqual(self.obr.testCrash(r), True)
        r1 = driftator.simulation.Robot("Driftator", 100, 80, 0, 5, 15, 200)
        self.assertEqual(self.obr.testCrash(r1), True)
        r2 = driftator.simulation.Robot("Driftator", 30, 50, 0, 5, 15, 200)
        self.assertEqual(self.obr.testCrash(r2), False)

if __name__ == "__main__":
    unittest.main()
