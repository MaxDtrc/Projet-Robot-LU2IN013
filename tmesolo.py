import driftator

simView = 1


strategie = None
config = None

def start(emetteur = False, deplacerEmetteur = False):
    try:
        driftator.startRobot("ia_tmesolo/" + strategie)
    except ImportError:
        driftator.startSimulation("ia_tmesolo/" + strategie, config, simView, 0.001, emetteur, deplacerEmetteur)


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

def q3_1():
    global strategie, config
    strategie = "exo3-1.ia"
    config = "config/config_q3.json"
    start(True)

def q3_2():
    global strategie, config
    strategie = "exo3-2.ia"
    config = "config/config_q3.json"
    start(True)

def q3_3():
    global strategie, config
    strategie = "exo3-3.ia"
    config = "config/config_q3.json"
    start(True, True)

q2_3()

    