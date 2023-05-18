import pygame
from math import sqrt, radians, degrees
import json
import argparse


#Lecture des arguments
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="default.json", dest="config", help="Config à éditer")
parser.add_argument("-f", "--fond", default="", dest="fond", help="Fond de l'éditeur (pour placer un repère)")
args=parser.parse_args()

#Taille du terrain
s_x = 152
s_y = 152

#Listes des obstacles [rectangles, ronds, robots, balises]
lst_obstacles = [[], [], [], []]

#Clefs utiles pour chacune des listes (pour ne garder que le necessaire)
clefs_utiles = [["posX", "posY", "longueur", "largeur"], ["posX", "posY", "rayon"], ["posX", "posY", "angle"], ["posX", "posY", "angle", "type_balise"]]

#Variables générales
pressing = False #Utilisateur en train de cliquer
nb_outils = 7 #Nombre d'outils
current = 0 #Outil sélectionné
e = 5 #Echelle

#Init de pygame
COULEUR_OBSTACLES = (65, 0, 55)

pygame.init()
screen = pygame.display.set_mode((s_x * e + 70, s_y * e))

pygame.display.set_caption('Editeur de configuration') 
screen.fill((255,255,255))

#Repère de fond
imgFond = None
if args.fond != "":
    imgFond = pygame.image.load(args.fond).convert_alpha()
    imgFond = pygame.transform.scale(imgFond, (s_x * e, s_y * e))


#Chargement des images
imgRobot = pygame.transform.scale(pygame.image.load("driftator/driftator/affichage/textures/robot.png").convert_alpha(), (15 * e, 19.5 * e))
balises_img = [pygame.transform.scale(pygame.image.load("driftator/driftator/affichage/textures/balise" + str(i) + ".png").convert_alpha(), (7 * e, 7 * e)) for i in range(1, nb_outils - 2)]


def getMouse():
    """
    Fonction retournant la position de la souris
    """
    x, y = pygame.mouse.get_pos()
    x = min(x, s_x * e)
    x = x/e - s_x/2
    y = y/e - s_y/2
    return x, y

def show_menu():
    """
    Fonction affichant le menu latéral
    """
    global screen

    clr_cases = (255, 112, 102)
    clr_selected = (255, 17, 0)

    #Affichage de la barre de séparation
    pygame.draw.rect(screen, (0, 0, 0), (s_x * e + 1, 0, 1, s_y * e))

    #Affichage de l'élément en cours
    pygame.draw.rect(screen, clr_selected, (s_x * e + 7, 7 + 65 * current, 56, 56))

    #Affichage des rectangles de fond
    for i in range(10, 10 + 65 * nb_outils, 65):
        pygame.draw.rect(screen, clr_cases, (s_x * e + 10, i, 50, 50))

    #Affichage des outils
    pygame.draw.rect(screen, COULEUR_OBSTACLES, (s_x * e + 20, 20, 30, 30)) #Rectangle
    pygame.draw.circle(screen, COULEUR_OBSTACLES, (s_x * e + 35, 100), 18)  #Cercle
    screen.blit(pygame.transform.scale(imgRobot, (imgRobot.get_width() * 0.5, imgRobot.get_height() * 0.5)), (s_x * e + 15, 140)) #Robot
    for i in range(nb_outils - 3): 
        screen.blit(pygame.transform.scale(balises_img[i], (balises_img[i].get_width(), balises_img[i].get_height())), (s_x * e + 17, 212 + 65 * i)) #Balises

def check_menu():
    """
    Fonction de detection de l'outil sélectionné
    """
    global current
    x, y = pygame.mouse.get_pos()

    if x <= s_x * e:
        return False #Le curseur n'est pas dans le menu
    
    #Detection de l'outil cliqué
    if s_x * e + 10 < x < s_x * e + 60 and 10 < y < 60 + 65 * nb_outils:
        current = (y - 10) // 65
        
    return True

def save():
    """
    Fonction permettant de sauvegarder une configuration
    """
    d = dict()
    d["terrain"] = {"tailleX": s_x, "tailleY": s_y}
    d["obstaclesRonds"] = [{**{"nom": "obstrond" + str(i)}, **o} for o, i in list(zip(lst_obstacles[1], [j for j in range(len(lst_obstacles[0]))]))]
    d["obstaclesRectangles"] = [{**{"nom": "obstrect" + str(i)}, **o} for o, i in list(zip(lst_obstacles[0], [j for j in range(len(lst_obstacles[0]))]))]
    d["robots"] = [{**{"nom": "robot" + str(i)}, **o} for o, i in list(zip(lst_obstacles[2], [j for j in range(len(lst_obstacles[2]))]))]
    d["balises"] = [{**{"nom": "balise" + str(i)}, **o} for o, i in list(zip(lst_obstacles[3], [j for j in range(len(lst_obstacles[3]))]))]
   
    with open("config/" + args.config, "w") as json_file:
        json_file.write(json.dumps(d, indent=4))

def load():
    """
    Fonction permettant de charger une configuration
    """
    global s_x, s_y, lst_obstacles

    with open("config/" + args.config, "r") as json_file:
        data = json.load(json_file)
        lst_obstacles = [data["obstaclesRectangles"], data["obstaclesRonds"], data["robots"], data["balises"]]



"""
Script principal
"""


#On charge la config passée en paramètres
load()

#Boucle principale
while True:
    #On reset l'ecran
    screen.fill((255,255,255))

    #On affiche le fond
    if imgFond is not None:
        screen.blit(imgFond, (0, 0))

    #On ajoute l'obstacle courant s'il existe
    if pressing:
        x2, y2 = getMouse()
        lst_obstacles[min(3, current)].append({"posX": (x1 + x2)/2 if current == 0 else x1, "posY": (y1 + y2)/2 if current == 0 else y1, "longueur": abs(x1 - x2), "rayon": int(sqrt((x2 - x1)**2 + (y2 - y1)**2)), "largeur": abs(y1 - y2), "angle": int(sqrt((x2 - x1)**2 + (y2 - y1)**2)%360) * 5 - 90, "type_balise": current - 2})
    
    #On affiche les obstacles
    for o in lst_obstacles[0]:
        pygame.draw.rect(screen, COULEUR_OBSTACLES, ((o["posX"] - o["longueur"]/2 + s_x/2) * e, (o["posY"] - o["largeur"]/2 + s_y/2) * e, o["longueur"] * e, o["largeur"] * e))
    
    for o in lst_obstacles[1]:
        pygame.draw.circle(screen, COULEUR_OBSTACLES, ((o["posX"] + s_x/2) * e, (o["posY"] + s_x/2) * e), o["rayon"] * e)

    for o in lst_obstacles[2]:
        i = pygame.transform.rotate(imgRobot, o["angle"])
        screen.blit(i, ((o["posX"] + s_x/2) * e - i.get_width()/2, (o["posY"] + s_y/2) * e - i.get_height()/2))

    for o in lst_obstacles[3]:
        i = pygame.transform.rotate(balises_img[o["type_balise"] - 1], o["angle"] + 90)
        screen.blit(i, ((o["posX"] + s_x/2) * e - i.get_width()/2, (o["posY"] + s_y/2) * e - i.get_height()/2))

    #On supprime l'élement courant des listes
    if pressing:
        lst_obstacles[min(3, current)].pop()

    #On update
    show_menu()
    pygame.display.update()

    #Lecture des events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit() #On arrête.

        #Clic gauche -> On commence à dessiner un obstacle
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x1, y1 = getMouse()
            if not check_menu():
                pressing = True

        #Relachement du clic gauche -> On ajoute l'obstacle
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x2, y2 = getMouse()
            if not check_menu():
                all_values = {"posX": (x1 + x2)/2 if current == 0 else x1, "posY": (y1 + y2)/2 if current == 0 else y1, "longueur": abs(x1 - x2), "largeur": abs(y1 - y2), "rayon": int(sqrt((x2 - x1)**2 + (y2 - y1)**2)), "angle": int(sqrt((x2 - x1)**2 + (y2 - y1)**2)%360 * 5 - 90), "type_balise": current - 2}
                filtered = {k: v for k, v in all_values.items() if k in clefs_utiles[min(current, 3)]}
                lst_obstacles[min(current, 3)].append(filtered)

            pressing = False

        #Clic droit de la souris pour supprimer un élément
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = getMouse()

            for o in lst_obstacles[0]:
                if o["posX"] - o["longueur"]/2 <= x <= o["posX"] + o["longueur"]/2 and o["posY"] - o["largeur"]/2 <= y <= o["posY"] + o["largeur"]/2:
                    lst_obstacles[0].remove(o)
            for o in lst_obstacles[1]:
                if sqrt((o["posX"] - x)**2 + (o["posY"] - y)**2) <= o["rayon"]:  
                    lst_obstacles[1].remove(o)
            for o in lst_obstacles[2]:
                if sqrt((o["posX"] - x)**2 + (o["posY"] - y)**2) <= 5.85:  
                    lst_obstacles[2].remove(o)
            for o in lst_obstacles[3]:
                if sqrt((o["posX"] - x)**2 + (o["posY"] - y)**2) <= 7:  
                    lst_obstacles[3].remove(o)

        #Raccourci claviers pour sauvegarder/
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save()
            elif event.key == pygame.K_l:
                load()
