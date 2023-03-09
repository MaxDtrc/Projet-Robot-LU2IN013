from threading import Thread
import time
from math import pi, radians, degrees


TAILLE_ROUES = 7
RAYON_ROBOT = 5

"""def chargerIA(fichier: str, controleur):
    Création d'une séquence d'IA depuis un fichier
    
    :param fichier: nom du fichier
    :param controleur: controleur pour l'IA
    loop = False
    lst = []
    with open(fichier, 'r') as f:
        l = f.readline()
        while l:
            t = l.split(" ")
            match t[0]:
                case "avancer":
                    lst.append(Avancer(controleur, int(t[1]), int(t[2])))
                case "tourner_droite":
                    lst.append(TournerDroite(controleur, int(t[1]), int(t[2])))
                case "approcher_mur":
                    lst.append(ApprocherMur(controleur, int(t[1])))
                case "boucler":
                    loop = True
            l = f.readline()
    return (lst, loop)"""


class IA(Thread):
    """
    Classe représentant l'IA
    """
    def __init__(self, controleur, strat, dT):
        super(IA, self).__init__()
        self._controleur = controleur
        self.strategie = strat
        self._wait = dT/10

    def run(self):
        self.strategie.start()
        self._controleur.running = True
        while self._controleur.running:
            #Etape suivante
            self._lastTime = time.time()
            time.sleep(self._wait)
            self._dT = time.time() - self._lastTime
            self.step()

    def step(self):
        if not self.strategie.stop():
            self.strategie.step(self._dT)
        else:
            self.strategie.end()
            self._controleur.running = False


#IA de déplacement
class Avancer:
    """
    Classe représentant l'ia permettant d'avancer droit
    """
    def __init__(self, controleur, distance, v, angle = 0):
        self._controleur = controleur
        self.distance = distance
        self.angle = angle
        self.v = v
        self.parcouru = 0

    def start(self):
        self._controleur.getDistanceParcourue() #Reinitialisation
        self.parcouru = 0

    def stop(self):
        #On avance tant qu'on n'est pas trop près d'un mur/qu'on n' a pas suffisement avancé
        return self.parcouru > self.distance

    def step(self, dT: float):
        #Calcul de la distance parcourue
        self.parcouru += abs(self._controleur.getDistanceParcourue())

        if self.stop(): 
            self.end()
            return

        self.avancer()

    def end(self):
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

    def avancer(self):
        #Avancer selon l'angle et la vitesse
        if self.angle <= 0:
            self._controleur.setVitesseGauche(self.v * (1 + self.angle/100))
            self._controleur.setVitesseDroite(self.v)
        else:
            self._controleur.setVitesseGauche(self.v)
            self._controleur.setVitesseDroite(self.v * (1 - self.angle/100))

class TournerSurPlace:
    """
    Classe représentant l'ia permettant de tourner à droite
    """
    def __init__(self, controleur, angle, v):
        self._controleur = controleur
        self.angle = radians(angle)
        if angle >= 0:
            self.v = v
        else:
            self.v = -v
        self.parcouru = 0

    def start(self):
        self.parcouru = 0
        self._controleur.getDecalageAngle()
        
    def stop(self):
        #On tourne tant qu'on n'a pas dépassé l'angle
        return self.parcouru > abs(self.angle) 
        
    def step(self, dT : float):
        #Calcul de la distance parcourue
        a = abs(self._controleur.getDecalageAngle())
        self.parcouru += a
        
        if self.stop():
            self.end()
            return

        self.avancer()

    def end(self):
        self._controleur.setVitesseGauche(0)
        self._controleur.setVitesseDroite(0)

    def avancer(self):
        self._controleur.setVitesseGauche(self.v)
        self._controleur.setVitesseDroite(-self.v)

#IA constructionnelles
class IAIf:
    """
    Classe permettant de réaliser une ia conditionnelle
    """
    def __init__(self, controleur, ia1, ia2, condition):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia1: ia à appeler si la condition est vérifiée
        :param ia2: ia à appeler si la condition n'est pas vérifiée
        :param condition: IACondition correspondant à la condition du if
        """
        self._controleur = controleur
        self.v = 0
        self._ia1 = ia1
        self._ia2 = ia2
        self._condition = condition

    def start(self):
        #Initialisation des 2 sous IA
        self._condition.start()
        self._ia1.start()
        self._ia2.start()
        pass

    def stop(self):
        #Arrêt si l'une des deux IA est finie
        return self._ia1.stop() or self._ia2.stop()

    def step(self, dT: float):
        if not self._condition.stop():
            self._condition.step()
        else:
            if self.stop(): 
                self.end()
                return
            else:
                if self._condition.resultat:
                    self._ia1.step(dT)
                else:
                    self._ia2.step(dT)
            self._condition.start()
    
    def end(self):
        self._ia1.end()
        self._ia2.end()

class IAWhile:
    """
    Classe permettant de réaliser une ia tant qu'une condition est vérifiée
    """
    def __init__(self, controleur, ia, condition):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia: ia à appeler tant que la condition est vérifiée
        :param condition: IACondition correspondant à la condition du while
        """
        self._controleur = controleur
        self._ia = ia
        self._condition = condition

    def start(self):
        #Initialisation de la sous IA
        self._condition.start()
        self._ia.start()
        pass

    def stop(self):
        #Arrêt si la condition n'est pas vérifiée
        if not self._condition.stop():
            self._condition.step()
        if not self._condition.resultat:
            return True
        self._condition.start()

    def step(self, dT: float):
        if self.stop(): 
            self.end()
            return
        else:
            #Reset de l'IA
            if self._ia.stop():
                self._ia.end()
                self._ia.start()

            #Step
            self._ia.step(dT)
    
    def end(self):
        self._ia.end()

class IAFor:
    """
    Classe permettant de réaliser une ia un certain nombre de fois
    """
    def __init__(self, controleur, ia, nbIter):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia: ia à appeler si la condition est vérifiée
        :param condition: fonction de la condition qui renvoie un booléen
        """
        self._controleur = controleur
        self.v = 0
        self._ia = ia
        self._nbIter = nbIter

    def start(self):
        #Initialisation des 2 sous IA
        self._i = 0
        self._ia.start()
        pass

    def stop(self):
        #Arrêt si l'une des deux IA est
        if self._ia.stop():
            self._i += 1
            if(self._i >= self._nbIter):
                return True
            else:
                self._ia.end()
                self._ia.start()

    def step(self, dT: float):
        if self.stop(): 
            self.end()
            return
        else:
            self._ia.step(dT)
    
    def end(self):
        self._ia.end()

class IASeq:
    """
    Classe permettant de réaliser une séquence d'IA
    """
    def __init__(self, controleur, iaList):
        """
        Paramètres
        :param controleur: controleur du robot
        :param ia: ia à appeler si la condition est vérifiée
        :param condition: fonction de la condition qui renvoie un booléen
        """
        self._controleur = controleur
        self.v = 0
        self._iaList = iaList.copy()

    def start(self):
        #Initialisation de la sous ia 1
        self._i = 0
        self._iaList[self._i].start()

    def stop(self):
        #Passage à l'ia suivante si fini
        if self._iaList[self._i].stop():
            if(self._i >= len(self._iaList) - 1):
                return True
                

    def step(self, dT: float):
        if self.stop(): 
            self.end()
            return
        elif self._iaList[self._i].stop():
            self._iaList[self._i].end()
            self._i += 1
            self._iaList[self._i].start()
            
        self._iaList[self._i].step(dT)
    
    def end(self):
        self._iaList[self._i].end()

#IA complémentaires
class IACondition:
    """
    Classe permettant de réaliser une condition pour une IA
    """
    def __init__(self, controleur, args):
        """
        Paramètres
        :param controleur: controleur du robot
        :param args: Tableau splité de la condition
        """
        self._controleur = controleur
        self.resultat = None
        self._args = args

    def start(self):
        #Reset du resultat
        self.resultat = None
        self._vars = self._args.copy()

    def stop(self):
        #Arrêt si la condition a été testée
        return self.resultat != None

    def step(self):
        if not self.stop():
            for i in range(len(self._vars)):
                try:
                    #L'élément est une valeur
                    parsed = float(self._vars[i])
                except:
                    #L'élément est un nom de variable

                    #Si appel au capteur de distance, on le met à jour
                    if(self._vars[i] == "capteur_distance"):
                        self._controleur._variables["capteur_distance"] = self._controleur.getDistance()

                    #On substitue la variable à sa valeur
                    if(self._vars[i] not in ['(', ')', '==', '!=', '<', '>', '<=', '>=', '+', '-', '/', '*', '%', '//', 'and', 'or']):
                        self._vars[i] = str(self._controleur._variables[self._vars[i]])

            self.resultat = eval(' '.join(self._vars))
    
    def end(self):
        pass

class IAGererVariable:
    """
    Classe permettant de modifier une variable
    """
    def __init__(self, controleur, args):
        """
        Paramètres
        :param controleur: controleur du robot
        :param args: Tableau splité de l'instruction
        """
        self._controleur = controleur
        self.effectue = False
        self._args = args

    def start(self):
        #Reset du resultat
        self.effectue = False
        self._vars = self._args.copy()

    def stop(self):
        #Arrêt si l'instruction a été effectuée
        return self.effectue != False

    def step(self, dT):
        if not self.stop():
            for i in range(2, len(self._vars)):
                try:
                    #L'élément est une valeur
                    parsed = float(self._vars[i])
                except:
                    #L'élément est un nom de variable

                    #Si appel au capteur de distance, on le met à jour
                    if(self._vars[i] == "capteur_distance"):
                        self._controleur._variables["capteur_distance"] = self._controleur.getDistance()

                    #On substitue la variable à sa valeur
                    if(self._vars[i] not in ['(', ')', '==', '!=', '<', '>', '<=', '>=', '+', '-', '/', '*', '%', '//']):
                        self._vars[i] = str(self._controleur._variables[self._vars[i]])

            self._controleur._variables[self._args[0]] = eval(''.join(self._vars[2:]))
            self.effectue = True

    def end(self):
        pass

class IAPrint:
    """
    Classe permettant d'effectuer un affichage
    """
    def __init__(self, controleur, args):
        """
        Paramètres
        :param controleur: controleur du robot
        :param args: Tableau splité de l'instruction
        """
        self._controleur = controleur
        self.effectue = False
        self._args = args

    def start(self):
        #Reset du resultat
        self.effectue = False
        self._vars = self._args.copy()

    def stop(self):
        #Arrêt si l'instruction a été effectuée
        return self.effectue != False

    def step(self, dT):
        if not self.stop():
            for i in range(len(self._vars)):
                try:
                    #L'élément est une valeur
                    parsed = float(self._vars[i])
                except:
                    #L'élément est un nom de variable

                    #Si appel au capteur de distance, on le met à jour
                    if(self._vars[i] == "capteur_distance"):
                        self._controleur._variables["capteur_distance"] = self._controleur.getDistance()

                    #On substitue la variable à sa valeur
                    if(self._vars[i] not in ['(', ')', '==', '!=', '<', '>', '<=', '>=', '+', '-', '/', '*', '%', '//']):
                        self._vars[i] = str(self._controleur._variables[self._vars[i]])

            #Affichage
            print(eval(''.join(self._vars)))
            self.effectue = True

    def end(self):
        pass



#Parser d'IA
def readIA(ia, c):
    i = 0
    seq = []
    while(i < len(ia)):
        #Commentaire ou blanc
        if ia[i] == '\n' or (len(ia[i]) > 2 and ia[i][:2] == '//'):
            i+=1
        
        #Instruction "avancer"
        elif len(ia[i]) >= 7 and ia[i][:7] == 'avancer':
            #Découpage de la commande
            instr = ia[i].split(' ')

            #Creation des variables
            d = 0
            v = 0
            a = 0
            
            #Lecture de la commande
            for j in instr[1:]:
                #suppression du \n
                if j[-1] == '\n':
                    j = j[:-2]
                
                #Lecture des jiables
                if j[0] == 'd':
                    d = float(j[2:])
                elif j[0] == 'v':
                    v = float(j[2:])
                elif j[0] == 'a':
                    a = float(j[2:])

            #Ajout de la commande
            seq.append(Avancer(c, d, v, a))
            i+=1
        
        #Instruction "tourner"
        elif len(ia[i]) >= 7 and ia[i][:7] == 'tourner':
            #Découpage de la commande
            instr = ia[i].split(' ')

            #Creation des variables
            a = 0
            v = 0
            
            #Lecture de la commande
            for j in instr[1:]:
                #suppression du \n
                if j[-1] == '\n':
                    j = j[:-2]
                
                #Lecture des jiables
                if j[0] == 'a':
                    a = float(j[2:])
                elif j[0] == 'v':
                    v = float(j[2:])

            #Ajout de la commande
            seq.append(TournerSurPlace(c, a, v))
            i+=1
        
        #Instruction "For"
        elif len(ia[i]) >= 3 and ia[i][:3] == 'for':
            #Lecture du nombre de fois à repeter
            nb = int(ia[i].split('(')[1].split(')')[0])

            #Lecture des instructions
            i+=1
            nbParenthOuverte = 0
            tabBloc = []
            while ia[i][0] != '}' or nbParenthOuverte != 0:
                #Suppression des indentations:
                while(ia[i][0] == ' '):
                    ia[i] = ia[i][1:]

                #Detection d'une parenthèse ouvrante
                if(len(ia[i]) >= 2 and ia[i][-2] == '{'):
                    nbParenthOuverte += 1

                #Detection d'une parenthèse fermante
                if(len(ia[i]) >= 2 and ia[i][-2] == '}'):
                    nbParenthOuverte += -1

                #Ajout de la commande
                tabBloc.append(ia[i])
                i+=1
            blocIA = readIA(tabBloc, c)

            #Ajout de la commande
            seq.append(IAFor(c, blocIA, nb))
            i+=1
        
        #Instruction "If"
        elif len(ia[i]) >= 2 and ia[i][:2] == 'if':
            #Lecture de la condition
            cond = ia[i].split('(')[1].split(')')[0].split(' ')
            
            #Creation de la condition
            iaCond = IACondition(c, cond)

            #Lecture des deux blocs
            i+=1
            nbParenthOuverte = 0
            tabBloc = []
            while ia[i][0] != '}' or nbParenthOuverte != 0:
                #Suppression des indentations:
                while(ia[i][0] == ' '):
                    ia[i] = ia[i][1:]

                #Detection d'une parenthèse ouvrante
                if(len(ia[i]) >= 2 and ia[i][-2] == '{'):
                    nbParenthOuverte += 1

                #Detection d'une parenthèse fermante
                if(len(ia[i]) >= 2 and ia[i][-2] == '}'):
                    nbParenthOuverte += -1

                #Ajout de la commande
                tabBloc.append(ia[i])
                i+=1
            blocIA1 = readIA(tabBloc, c)

            i+=2
            tabBloc = []
            while ia[i][0] != '}' or nbParenthOuverte != 0:
                #Suppression des indentations:
                while(ia[i][0] == ' '):
                    ia[i] = ia[i][1:]

                #Detection d'une parenthèse ouvrante
                if(len(ia[i]) >= 2 and ia[i][-2] == '{'):
                    nbParenthOuverte += 1

                #Detection d'une parenthèse fermante
                if(len(ia[i]) >= 2 and ia[i][-2] == '}'):
                    nbParenthOuverte += -1

                #Ajout de la commande
                tabBloc.append(ia[i])
                i+=1
            blocIA2 = readIA(tabBloc, c)

            #Ajout de la condition
            seq.append(IAIf(c, blocIA1, blocIA2, iaCond))
            i+=1
        
        #Instruction "While"
        elif len(ia[i]) >= 5 and ia[i][:5] == 'while':
            #Lecture de la condition
            cond = ia[i].split('(')[1].split(')')[0].split(' ')
            
            #Creation de la condition
            iaCond = IACondition(c, cond)

            #Lecture des deux blocs
            i+=1
            nbParenthOuverte = 0
            tabBloc = []
            while ia[i][0] != '}' or nbParenthOuverte != 0:
                #Suppression des indentations:
                while(ia[i][0] == ' '):
                    ia[i] = ia[i][1:]

                #Detection d'une parenthèse ouvrante
                if(len(ia[i]) >= 2 and ia[i][-2] == '{'):
                    nbParenthOuverte += 1

                #Detection d'une parenthèse fermante
                if(len(ia[i]) >= 2 and ia[i][-2] == '}'):
                    nbParenthOuverte += -1

                #Ajout de la commande
                tabBloc.append(ia[i])
                i+=1
            blocIA = readIA(tabBloc, c)

            #Ajout de la condition
            seq.append(IAWhile(c, blocIA, iaCond))
            i+=1
             
        #Print
        elif len(ia[i]) >= 5 and ia[i][:5] == 'print':
            #Lecture de la definition de variable et suppression du ;
            instr = ia[i].split('(')[1].split(')')[0].split(' ')

            #Ajout de l'instruction
            seq.append(IAPrint(c, instr))
            i+=1

        #Definition de variable
        elif (len(ia[i].split(' ')) >= 1 and ia[i].split(' ')[1] == '='):
            #Lecture de la definition de variable et suppression du ;
            instr = ia[i][:-2].split(" ")

            #Ajout de l'instruction
            seq.append(IAGererVariable(c, instr))
            i+=1
            
        
    return IASeq(c, seq)


def openIA(fichier, c, dT):
    with open(fichier, 'r') as f:
        s = f.readlines()
    return IA(c, readIA(s, c), dT)
        