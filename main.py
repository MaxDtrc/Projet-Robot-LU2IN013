import sys
import driftator

simView = int(sys.argv[1]) if len(sys.argv) >= 1 else 1
strategie = sys.argv[2] if len(sys.argv) >= 3 else "main.ia"
config = sys.argv[3] if len(sys.argv) >= 4 else "config/config_obst.json"

try:
    driftator.startRobot(strategie)
except ImportError:
    driftator.startSimulation(strategie, config, simView)
