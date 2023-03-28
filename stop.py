#Variables d'affichage (1 = 2d, 2 = 3d)
simView = 2
strategie = "stop.ia"

try:
    import driftator
    driftator.start(strategie)

except ImportError:
    import driftator_sim
    driftator_sim.start(strategie, simView)