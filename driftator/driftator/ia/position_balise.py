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
    r = np.where((img[..., 0:1] > 120) & (img[..., 0:1] > img[..., 1:2] * 1.6) & (img[..., 0:1] > img[..., 2:3] * 1.6))[1]
    b = np.where((img[..., 2:3] > 140) & (img[..., 2:3] > img[..., 0:1] * 4) & (img[..., 2:3] > img[..., 1:2] * 1.5))[1]
    v = np.where((img[..., 1:2] > 120) & (img[..., 1:2] > img[..., 2:3] * 2) & (img[..., 1:2] > img[..., 2:3] * 2))[1]
    j = np.where((img[..., 0:1] > 150) & (img[..., 1:2] > 150) & (img[..., 2:3] < 50))[1]

    clr_balises = [r, b, v, j]
    
    if np.prod([len(i) for i in clr_balises]) == 0:
        #Il manque une couleur
        return None
    
    #La couleur a bien été trouvée, on renvoie la coordonnée x
    clr = [np.mean(c) for c in clr_balises[id]]
    return 0, np.mean(clr)/80 - 1

def getPosBaliseV3(img):
    #Redimension de l'image
    img = Image.fromarray(img)
    img.save("test.png")
    print("image sauvée")
    img = img.resize((80, 60))
    img = np.array(img)

    #Obtention des coordonnées moyennes des couleurs rouge/bleu/vert/jaune
    j = np.where((img[..., 0:1] > 150) & (img[..., 1:2] > 150) & (img[..., 2:3] < 30))

    x = j[0]
    y = j[1]
    
    for p in len(x):
        #Coin au gauche
        top_left = (x[p], y[p])
        
        #Coin haut droite
        top_right = np.where((y == top_left[1]) & (x > top_left[0]))
        if len(top_right) == 0:
            break
        else:
            top_right = top_right[0]

        #Coin bas gauche
        bottom_left = np.where((x == top_left[0]) & (y > top_left[1]))
        if len(bottom_left) == 0:
            break
        else:
            bottom_left = bottom_left[0]

        #Coin bas droite
        bottom_right = np.where((x == top_right[0]) & (y > top_right[1]))
        if len(bottom_right) == 0:
            break
        else:
            bottom_right = bottom_right[0]

        balise_coordinates = (top_left, top_right, bottom_left, bottom_right)
        break

        
    #La couleur a bien été trouvée, on renvoie la coordonnée x
    return 0, (balise_coordinates[0] + balise_coordinates[1])/80 - 1


def getBalises(img):
    #Redimension de l'image
    img = Image.fromarray(img)
    width, height = int(img.width/8), int(img.height/8)
    img = img.resize((width, height), Image.NEAREST)

    #Conversion en HSV et conservation du canal 'hue' uniquement
    img = img.convert('HSV')
    img = np.array(img)[:,:,0]

    #On cherche les carrés jaunes
    j = np.where((img > 30) & (img < 60))
    
    #Recherche des coins
    bs = 4 #Taille des intervalles pour l'histogramme

    
    hist = np.histogram(j[0], bins = [b * bs for b in range(int(width/bs))])[0] #On fait l'histogramme en y
    y = [e * bs + bs//2 for e in np.sort(np.argsort(hist)[-2:])] if np.any(hist) else None
    if y is None or len(y) < 2 or abs(y[0] - y[1]) < 2 * bs:
        return None, None
    
    hist = np.histogram(j[1], bins = [b * bs for b in range(int(height/bs))])[0] #On fait l'histogramme en x
    x = [e * bs + bs//2 for e in np.sort(np.argsort(hist)[-2:])] if np.any(hist) else None
    if x is None or len(x) < 2 or abs(x[0] - x[1]) < 2 * bs:
        return None, None


    t = img[y[0]:y[1], x[0]:x[1]] #On ne retient que la partie de l'image qui correspond à la balise

    b = np.where((t > 150) & (t < 270)) #On récupère les coordonnées des points bleus

    if len(b[0]) == 0:
        return None, None

    y_coord, x_coord = np.mean(b[0]/len(t)), np.mean(b[1]/len(t[0])) #On obtient les coordonnées moyennes en x/y

    #Valeur droite/haut
    res = (1 if x_coord > 0.5 else 0, 1 if y_coord < 0.5 else 0) #On détermine si le carré bleu est à droite et/ou en haut


    pos_balise = ((x[0] + x[1])/2)/(width/2) - 1
    id_balise = [(0, 1), (0, 0), (1, 0), (1, 1)].index(res) + 1

    return pos_balise, id_balise