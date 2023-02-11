from threading import Thread
import time

class IA(Thread):
    def __init__(self, controleur):
        super(IA, self).__init__()
        self._controleur = controleur

    def run(self):
        while True:
            self.step()
            time.sleep(0.1)
        

    def step(self):
        pass