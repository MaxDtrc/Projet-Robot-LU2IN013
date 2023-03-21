from .ia import *

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
                
                #Lecture des variables
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
                
                #Lecture des variables
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
            nb = ia[i].split('(')[1].split(')')[0]

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