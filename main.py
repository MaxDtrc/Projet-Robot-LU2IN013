simView = 2
strategie = "main.ia"
config = "config/config_sans_obst.json"

try:
    import driftator
    driftator.start(strategie)

except ImportError:
    import driftator_sim
    driftator_sim.start(strategie, config, simView)