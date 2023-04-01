import driftator

simView = 1
strategie = "demo_ia/test2.ia"
config = "config/config_obst.json"

try:
    driftator.startRobot(strategie)
except ImportError:
    driftator.startSimulation(strategie, config, simView)



    