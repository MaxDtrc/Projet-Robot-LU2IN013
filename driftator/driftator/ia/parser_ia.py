from .ia import *

instructions = {"avancer": Avancer, "tourner_tete": TournerTete, "tourner": TournerSurPlace, "stop": Stop}

def readIA(ia, c):
    """
    Fonction permettant de parser une IA (str)

    :param ia: ia à parser
    :param c: controleur
    """
    i = 0
    seq = []

    while(i < len(ia)):
        splited = ia[i].replace('\n', '').split(" ")

        #Commentaire ou blanc
        if ia[i] == '\n' or (len(ia[i]) > 2 and ia[i][:2] == '//'):
            i+=1
        
        #Instructions de base (avancer, tourner, tourner_tete, stop)
        elif len(ia[i]) >= 1 and splited[0] in instructions.keys():
            #Ajout de la commande
            seq.append(eval("instructions['" + splited[0] + "'](c=c, " + ','.join(splited[1:]) + ")"))

        
        #Instruction "For"
        elif len(ia[i]) >= 3 and ia[i][:3] == 'for':
            #On lit le nombre de fois à répéter, on lit le bloc et on crée l'IA
            nb = ia[i].split('(')[1].split(')')[0]
            blocIA, i = readBloc(ia, c, i)
            seq.append(IAFor(c, blocIA, nb))
        
        #Instruction "If"
        elif len(ia[i]) >= 2 and ia[i][:2] == 'if':
            #Lecture de la condition, lecture du ou des blocs puis création de l'IA
            cond = ia[i].split('(')[1].split(')')[0].split(' ')
            
            blocIA1, i = readBloc(ia, c, i)
            blocIA2 = None
            if(i == len(ia) - 1):
                pass
            elif(ia[i] == "}else{\n" or ia[i+1] == "else{\n"):
                i += 1 if ia[i+1] == "else{\n" else 0
                blocIA2, i = readBloc(ia, c, i)
                
            seq.append(IAIf(c, blocIA1, blocIA2, cond))
            
        #IA Alterner
        elif len(ia[i]) >= 8 and ia[i][:8] == 'alterner':
            #Lecture de la condition, lecture des blocs et création de l'IA
            iaCond = ia[i].split('(')[1].split(')')[0].split(' ')

            blocIA1, i = readBloc(ia, c, i)
            i += 1 if ia[i] != "}else{\n" else 0
            blocIA2, i = readBloc(ia, c, i)

            seq.append(IAAlterner(c, blocIA1, blocIA2, iaCond))

        #Instruction "While"
        elif len(ia[i]) >= 5 and ia[i][:5] == 'while':
            #On lit la condition, le bloc et on crée la condition
            iaCond = ia[i].split('(')[1].split(')')[0].split(' ')
            blocIA, i = readBloc(ia, c, i)
            seq.append(IAWhile(c, blocIA, iaCond))
             
        #Print
        elif len(ia[i]) >= 5 and ia[i][:5] == 'print':
            #Lecture de l'argument et construction de l'IA
            seq.append(IAFonction(c, ["printVariable"] + ia[i].split('(')[1].split(')')[0].split(' ')))

        #Definition de variable
        elif (len(ia[i].split(' ')) >= 2 and ia[i].split(' ')[1] == '='):
            #Lecture de l'instruction et construction de l'IA
            seq.append(IAFonction(c, ["affecterValeur"] + ia[i].replace('\n', '').split(" ")))
            
        i+=1
        
    return IASeq(c, seq)

def readBloc(ia, c, i):
    """
    Fonction permettant de lire un bloc

    :param ia: ia à lire
    :param c: controleur
    :param i: ligne à lire
    """
    i+=1
    nbParenthOuverte = 0
    tabBloc = []
    while ia[i][0] != '}' or nbParenthOuverte != 0:
        #Suppression des indentations:
        while(ia[i][0] == ' '):
            ia[i] = ia[i][1:]

        #Detection des parenthèses
        nbParenthOuverte += 1 if '{' in ia[i] else 0
        nbParenthOuverte -= 1 if '}' in ia[i] else 0

        #Ajout de la commande
        tabBloc.append(ia[i])
        i+=1

    return readIA(tabBloc, c), i
        
def openIA(fichier, c, dT):
    """
    Fonction permettant d'ouvrir une IA

    :param fichier: fichier à lire
    :param c: controleur sur lequel appliquer l'IA
    :param dT: dT entre deux appels à l'IA
    """
    with open(fichier, 'r') as f:
        s = f.readlines()
    return IA(c, readIA(s, c), dT)