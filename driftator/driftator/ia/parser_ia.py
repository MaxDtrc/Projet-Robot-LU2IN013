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
            d = "0"
            v = "0"
            a = "0"
            
            #Lecture de la commande
            for j in instr[1:]:
                #suppression du \n
                if j[-1] == '\n':
                    j = j[:-1]
                
                #Lecture des variables
                if j[0] == 'd':
                    d = j[2:]
                elif j[0] == 'v':
                    v = j[2:]
                elif j[0] == 'a':
                    a = j[2:]

            #Ajout de la commande
            seq.append(Avancer(c, d, v, a))
            i+=1
        
        #Instruction "tourner"
        elif len(ia[i]) >= 7 and ia[i][:7] == 'tourner':
            #Découpage de la commande
            instr = ia[i].split(' ')

            #Creation des variables
            a = "0"
            v = "0"
            
            #Lecture de la commande
            for j in instr[1:]:
                #suppression du \n
                if j[-1] == '\n':
                    j = j[:-1]
                
                #Lecture des variables
                if j[0] == 'a':
                    a = j[2:]
                elif j[0] == 'v':
                    v = j[2:]

            #Ajout de la commande
            seq.append(TournerSurPlace(c, a, v))
            i+=1

        #Instruction "stop"
        elif len(ia[i]) >= 4 and ia[i][:4] == 'stop':
            #Ajout de la commande
            seq.append(Stop(c))
            i+=1
        
        #Instruction "For"
        elif len(ia[i]) >= 3 and ia[i][:3] == 'for':
            #Lecture du nombre de fois à repeter
            nb = ia[i].split('(')[1].split(')')[0]

            #Lecture des instructions
            blocIA, i = readBloc(ia, c, i)

            #Ajout de la commande
            seq.append(IAFor(c, blocIA, nb))
            i+=1
        
        #Instruction "If"
        elif len(ia[i]) >= 2 and ia[i][:2] == 'if':
            #Lecture de la condition
            cond = ia[i].split('(')[1].split(')')[0].split(' ')
            
            #Lecture des deux blocs
            blocIA1, i = readBloc(ia, c, i)

            blocIA2 = None
            
            if(i == len(ia) - 1):
                pass
            elif(ia[i] == "}else{\n"):
                blocIA2, i = readBloc(ia, c, i)
            elif(ia[i+1] == "else{\n"):
                i+=1
                blocIA2, i = readBloc(ia, c, i)
                
            i+=1
            #Ajout de la condition
            seq.append(IAIf(c, blocIA1, blocIA2, cond))
            

        #IA Alterner
        elif len(ia[i]) >= 8 and ia[i][:8] == 'alterner':
            #Lecture de la condition
            iaCond = ia[i].split('(')[1].split(')')[0].split(' ')

            #Lecture des deux blocs
            blocIA1, i = readBloc(ia, c, i)
            if(ia[i] == "}else{\n"):
                blocIA2, i = readBloc(ia, c, i)
            else:
                print(ia[i])
                i+=1
                blocIA2, i = readBloc(ia, c, i)

            i+=1
            #Ajout de la condition
            seq.append(IAAlterner(c, blocIA1, blocIA2, iaCond))

        
        #Instruction "While"
        elif len(ia[i]) >= 5 and ia[i][:5] == 'while':
            #Lecture de la condition
            iaCond = ia[i].split('(')[1].split(')')[0].split(' ')
            
            #Lecture des deux blocs
            blocIA, i = readBloc(ia, c, i)

            #Ajout de la condition
            seq.append(IAWhile(c, blocIA, iaCond))
            i+=1
             
        #Print
        elif len(ia[i]) >= 5 and ia[i][:5] == 'print':
            #Lecture de la definition de variable et suppression du ;
            instr = ia[i].split('(')[1].split(')')[0].split(' ')

            #Ajout de l'instruction
            seq.append(IAFonction(c, ["printVariable"] + instr))
            i+=1

        #Definition de variable
        elif (len(ia[i].split(' ')) >= 1 and ia[i].split(' ')[1] == '='):
            #Lecture de la definition de variable
            instr = ia[i].replace('\n', '').split(" ")

            #Ajout de l'instruction
            seq.append(IAFonction(c, ["affecterValeur"] + instr))
            i+=1
            
        
    return IASeq(c, seq)

def readBloc(ia, c, i):
    i+=1
    nbParenthOuverte = 0
    tabBloc = []
    while ia[i][0] != '}' or nbParenthOuverte != 0:
        #Suppression des indentations:
        while(ia[i][0] == ' '):
            ia[i] = ia[i][1:]

        #Detection d'une parenthèse ouvrante
        if('{' in ia[i]):
            nbParenthOuverte += 1

        #Detection d'une parenthèse fermante
        if('}' in ia[i]):
            nbParenthOuverte += -1

        #Ajout de la commande
        tabBloc.append(ia[i])
        i+=1
    return readIA(tabBloc, c), i
        

def openIA(fichier, c, dT):
    with open(fichier, 'r') as f:
        s = f.readlines()
    return IA(c, readIA(s, c), dT)