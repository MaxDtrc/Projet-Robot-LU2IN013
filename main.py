import driftator
import driftator_sim

#Variables d'affichage (1 = 2d, 2 = 3d)
simView = 1

strategie = "test2.ia"

try:
    driftator.start(strategie)

except ImportError:
    driftator_sim.start(strategie, simView)