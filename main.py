simView = 2
strategie = "demo_ia/test2.ia"
config = "config/config_obst.json"

try:
    import driftator
    driftator.start(strategie)

except ImportError:
    import driftator_sim
    driftator_sim.start(strategie, config, simView)