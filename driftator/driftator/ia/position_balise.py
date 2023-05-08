import numpy as np
from PIL import Image

def setColor(clr):
    """
    Fonction auxiliaire permettant de remplacer une valeur rgb par un id de couleur

    :param clr: tableau d'une valeur rgb
    :returns: un identifiant (1 à 5) selon la couleur
    """
    d = 0
    #Detection rouge
    if clr[0] > 85 and clr[0] > clr[1] * 1.6 and clr[0] > clr[2] * 1.6:
        d = 1
    #Detection vert
    elif clr[1] > 50 and clr[1] > clr[0] * 1.3 and clr[1] > clr[2] * 1.3:
        d = 2
    #Detection bleu
    elif clr[2] > 70 and clr[2] > clr[1] * 1.3 and clr[2] > clr[0] * 1.3:
        d = 3
    #Detection jaune
    elif clr[0] > 80 and clr[1] > 80 and clr[1] > 1.6 * clr[2] and clr[0] > 1.6 * clr[2]:
        d = 4
    return d

def distanceCase(v1, v2):
    """
    Fonction auxiliaire renvoyant une distance en nb de case entre 2 couples de coordonnées    
    """
    return abs(v1[0] - v2[0]) + abs(v1[1] - v2[1])

def getPosBalise(img):
    #Lecture de l'image
    im = Image.fromarray(img)


    #Redimension de l'image pour simplifier les calculs + conversion en array
    im = im.resize((16, 12), Image.NEAREST)

    im.save("test.png")
    m = np.array(im)

    #On remplace les pixels par l'id de leur couleur
    m = np.array([[setColor(i) for i in j] for j in m])
    
    #On stock les occurences des couleurs
    clr = [np.where(m==i+1) for i in range(4)]

    if (np.any(len(clr) == 0)):
        #Toutes les couleurs n'ont pas été trouvées, inutile de continuer
        return None

    #On crée les listes de coordonnées
    lst = [np.column_stack((np.array(clr[i])[0], np.array(clr[i])[1])) for i in range(4)]

    #On compte les occurences des couleurs (dans clr qui ne sert plus par la suite)
    clr = [len(i[0]) for i in clr]

    #On crée une liste d'ordre de parcours (croissant pour économiser les calculs)
    v = np.argsort(clr)
        
    n = 6 #Marge de recherche

    #Pour chaque occurence la couleur, on regarde si les autres couleurs sont présentes autour
    for p1 in lst[v[0]]:
        #Tableau des couleurs trouvées dans la zone
        clr_trouvees = [False, False, False, False]
        clr_trouvees[v[0]] = True

        #On parcours toutes les autres couleurs
        for c in v[1:]:
            #Dans cette couleur, on parcours les pixels
            for p2 in lst[c]:
                if distanceCase(p1, p2) < n:
                    #La couleur est trouvée, on sort de la boucle
                    clr_trouvees[c] = True
                    break

        if clr_trouvees.count(True) == 4:
            #La balise est trouvée, on retourne sa position x (Entre -1 et 1, -1 -> Tout à gauche de l'écran, 1 -> tout à droite de l'écran)
            return (p1[1] - 7)/8
        
    #Si la balise n'a pas été trouvée, on renvoie -2
    return None

def getPosBaliseV2(img):
    #Redimension de l'image
    img = Image.fromarray(img)
    img = img.resize((160, 120))
    img = np.array(img)

    #Obtention des coordonnées moyennes des couleurs rouge/bleu/vert/jaune
    r = np.where((img[..., 0:1] > 85) & (img[..., 0:1] > img[..., 1:2] * 1.6) & (img[..., 0:1] > img[..., 2:3] * 1.6))[1]
    b = np.where((img[..., 2:3] > 70) & (img[..., 2:3] > img[..., 0:1] * 1.3) & (img[..., 2:3] > img[..., 1:2] * 1.1))[1]
    v = np.where((img[..., 0:1] > 80) & (img[..., 1:2] > 80) & (img[..., 1:2] > img[..., 2:3] * 1.6) & (img[..., 0:1] > img[..., 2:3] * 1.6))[1]
    j = np.where((img[..., 1:2] > 50) & (img[..., 1:2] > img[..., 0:1]) & (img[..., 1:2] > img[..., 2:3]))[1]

    ro =  np.where((img[..., 0:1] > 80) & (img[..., 1:2] < 200) & (img[..., 0:1] > img[..., 2:3] * 1.2))[1]
    vi =  np.where((img[..., 2:3] > 80) & (img[..., 1:2] < 200) & (img[..., 2:3] > img[..., 0:1] * 1.2))[1]
    o = np.where((img[..., 0:1] > 80) & (img[..., 2:3] < 200) & (img[..., 0:1] > img[..., 1:2] * 1.2))[1]

    wanted = [b, vi, ro, o]
    if np.prod([len(i) for i in wanted]) == 0:
        #Il manque une couleur
        return None
    
    #La couleur a bien été trouvée, on renvoie la coordonnée x
    clr = [np.mean(c) for c in wanted]
    return np.mean(clr)/80 - 1