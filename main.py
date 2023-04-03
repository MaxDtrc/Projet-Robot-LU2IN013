import driftator

simView = 1
strategie = "demo_ia/capteur_et_emetteur.ia"
config = "config/config_obst.json"

try:
    driftator.startRobot(strategie)
except ImportError:
    driftator.startSimulation(strategie, config, simView)



    