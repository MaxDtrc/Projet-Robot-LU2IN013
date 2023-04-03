import driftator

simView = 1
strategie = "demo_ia/hexagone.ia"
config = "config/config_sans_obst.json"

try:
    driftator.startRobot(strategie)
except ImportError:
    driftator.startSimulation(strategie, config, simView)



    