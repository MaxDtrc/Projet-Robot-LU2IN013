from threading import Thread

class IA(Thread):

    def __init__(self, controleur):
        super(IA, self).__init__()
        self._controleur = controleur
        self._vitesseG = None
        self._vitesseD = None

    def run(self):
        pass