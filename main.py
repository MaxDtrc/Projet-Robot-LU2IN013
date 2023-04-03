import driftator

simView = 1
strategie = "main.ia"
config = "config/config_q1.json"

try:
    driftator.startRobot(strategie)
except ImportError:
    driftator.startSimulation(strategie, config, simView)



    