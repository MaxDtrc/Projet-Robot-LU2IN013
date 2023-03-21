import numpy as np
import cv2

from direct.showbase.ShowBase import ShowBase

#On définit les bornes de valeurs HSV des différentes couleurs pour la reconnaissance 
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

lower_blue = np.array([90, 130, 0])
upper_blue = np.array([121, 255, 255])


lower_red_1 = np.array([0, 100, 100])
upper_red_1 = np.array([10, 255, 255])
lower_red_2 = np.array([170, 100, 100])
upper_red_2 = np.array([180, 255, 255])

lower_green = np.array([40, 70, 80])
upper_green = np.array([70, 255, 255])


def getPosBalise(img):
    """
    Renvoie la position détectée de la balise sur l'image
    
    :param img: image à analyser
    """

    #On la convertit pour avoir les données des couleurs
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    colors = [(lower_yellow, upper_yellow), (lower_blue, upper_blue), (lower_green, upper_green), (lower_red_1, upper_red_1), (lower_red_2, upper_red_2)]
    points_tab = [[], [], [], []]
    mask_tab = [None, None, None, None]
    contours_tab = [None, None, None, None]

    for i in (range(0, 4)):
        if i == 3:
            mask_tab[i] = cv2.inRange(image, colors[i][0], colors[i][1]) | cv2.inRange(image, colors[i+1][0], colors[i+1][1]) #Cas special pour le rouge
        else:
            mask_tab[i] = cv2.inRange(image, colors[i][0], colors[i][1])
        contours_tab[i], hierarchy = cv2.findContours(mask_tab[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #On détecte les contours de la zone trouvée
        if len(contours_tab[i]) != 0:
            for contour in contours_tab[i]:
                if cv2.contourArea(contour) > 500:
                    x, y, w, h = cv2.boundingRect(contour)
                    points_tab[i].append(np.array([x + int(w/2), y + int(h/2)]))

                    #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3) #Pour chaque contour trouvé on trace un rectangle autour
                    #cv2.circle(img, (x + int(w/2), y + int(h/2)), 4, (255, 0, 0), 5)

    #Croisement des points
    if len(points_tab[0]) > 0 and len(points_tab[1]) > 0 and len(points_tab[2]) > 00 and len(points_tab[3]) > 0:
        for py in points_tab[0]:
            for pb in points_tab[1]:
                for pg in points_tab[2]:
                    for pr in points_tab[3]:
                        #On calcule les centre des segments en diagonal
                        p1 = np.array([int(np.mean([pr[0], py[0]])), int(np.mean([pr[1], py[1]]))])
                        p2 = np.array([int(np.mean([pg[0], pb[0]])), int(np.mean([pg[1], pb[1]]))])


                        #Si les points sont pas trop loin alors on en déduit que c'est la balise
                        if np.linalg.norm(p1 - p2) < 20:
                            return p1[0]

    return 0