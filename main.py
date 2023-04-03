simView = 1

#q1.1
config = "config/config_obst.json"

#q1.4
config2 = "config/config_sans_obst.json"
strategie = "demo_ia/testhexagone.ia"

#q2.1
strategie2 = "demo_ia/1.ia"

#q2.2
strategie3 = "demo_ia/0.ia"

#q2.3
strategie4 = "demo_ia/01.ia"

#q2.5
strategie5 = "demo_ia/0101.ia"
config3 = "config/config3.json"

try:
    import driftator
    driftator.start(strategie2)

except ImportError:
    import driftator_sim
    driftator_sim.start(strategie2, config3, simView)


