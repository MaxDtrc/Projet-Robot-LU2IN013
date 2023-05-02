import driftator
import argparse

#Lecture des arguments
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--view", default=2, dest="view", help="Vue de la simulation (1 -> 2d, 2 -> 3d)")
parser.add_argument("-ia", "--ia", default="main.ia", dest="ia", help="Fichier .ia à executer")
parser.add_argument("-c", "--config", default="config/default.json", dest="config", help="Config .json de la simulation à charger")
args=parser.parse_args()

simView, strategie, config = int(args.view), args.ia, args.config

#Lancement du programme
try:
    driftator.startRobot(strategie)
except ImportError:
    driftator.startSimulation(strategie, config, simView)