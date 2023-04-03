import driftator

simView = 1


strategie = None
config = None

def start():
    try:
        driftator.startRobot(strategie)
    except ImportError:
        driftator.startSimulation(strategie, config, simView)


def exo1():
    global strategie, config
    strategie = "exo1.ia"
    config = "config/config_q1.json"
    start()


def q2_1():
    global strategie, config
    strategie = "exo2-1.ia"
    config = "config/config_q2.json"
    start()

def q2_2():
    global strategie, config
    strategie = "exo2-2.ia"
    config = "config/config_q2.json"
    start()

def q2_3():
    global strategie, config
    strategie = "exo2-3.ia"
    config = "config/config_q2.json"
    start()

def q2_4():
    global strategie, config
    strategie = "exo2-4.ia"
    config = "config/config_q2.json"
    start()


exo1()

    