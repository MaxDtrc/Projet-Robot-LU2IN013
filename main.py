simView = 1

#q1.1
config = "config/config_obst.json"

#q1.4
config2 = "config/config_sans_obst.json"
strategie = "demo_ia/testhexagone.ia"

try:
    import driftator
    driftator.start(strategie)

except ImportError:
    import driftator_sim
    driftator_sim.start(strategie, config2, simView)
