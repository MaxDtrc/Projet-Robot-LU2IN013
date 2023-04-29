import pygame
from math import sqrt, radians, degrees
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", default="default.json", dest="config", help="Config à éditer")
args=parser.parse_args()


s_x = 152
s_y = 152

current_obst = {}
lst_obstacles_rect = []
lst_obstacles_rond = []
lst_robots = []

pressing = False
current = "rectangle"

e = 5

#Init de pygame
COULEUR_OBSTACLES = (65, 0, 55)

pygame.init()
screen = pygame.display.set_mode((s_x * e + 70, s_y * e))

pygame.display.set_caption('Editeur de scene') 
screen.fill((255,255,255))

img = pygame.image.load("driftator/driftator/affichage/robot.png").convert_alpha()
img = pygame.transform.scale(img, (img.get_width()/15 * 5.85 * e, img.get_height()/15 * 5.85 * e))

#Rectification de la position de la souris
def getMouse():
    x, y = pygame.mouse.get_pos()
    x = min(x, s_x * e)
    x = x/e - s_x/2
    y = y/e - s_y/2
    return x, y

#Fonction d'affichage du menu
def show_menu():
    global screen

    clr_cases = (255, 112, 102)
    clr_selected = (255, 17, 0)

    #Affichage de la barre de séparation
    pygame.draw.rect(screen, (0, 0, 0), (s_x * e + 1, 0, 1, s_y * e))

    #Affichage de l'élément en cours
    if current == "rectangle":
        pygame.draw.rect(screen, clr_selected, (s_x * e + 7, 7, 56, 56))
    elif current == "cercle":
        pygame.draw.rect(screen, clr_selected, (s_x * e + 7, 72, 56, 56))
    elif current == "robot":
        pygame.draw.rect(screen, clr_selected, (s_x * e + 7, 137, 56, 56))

    #Outil rectangle
    pygame.draw.rect(screen, clr_cases, (s_x * e + 10, 10, 50, 50))
    pygame.draw.rect(screen, COULEUR_OBSTACLES, (s_x * e + 20, 20, 30, 30))

    #Outil cercle
    pygame.draw.rect(screen, clr_cases, (s_x * e + 10, 75, 50, 50))
    pygame.draw.circle(screen, COULEUR_OBSTACLES, (s_x * e + 35, 100), 18)

    #Outil robot
    pygame.draw.rect(screen, clr_cases, (s_x * e + 10, 140, 50, 50))
    screen.blit(pygame.transform.scale(img, (img.get_width() * 0.5, img.get_height() * 0.5)), (s_x * e + 15, 140))

    

#Fonction détectant un clic dans le menu
def check_menu():
    global current
    x, y = pygame.mouse.get_pos()

    if x <= s_x * e:
        return False
    
    if s_x * e + 10 < x < s_x * e + 60 and 10 < y < 60:
        current = "rectangle"
    elif s_x * e + 10 < x < s_x * e + 60 and 75 < y < 125:
        current = "cercle"
    elif s_x * e + 10 < x < s_x * e + 60 and 140 < y < 190:
        current = "robot"

    return True

#Fonction pour sauvegarder la config
def save(robots, rectangles, ronds, s_x, s_y):
    """
    Fonction permettant de sauvegarder une configuration
    """
    d = dict()
    d["terrain"] = {"tailleX": s_x, "tailleY": s_y}
    d["obstaclesRonds"] = [{**{"nom": "obstrond" + str(i)}, **o} for o, i in list(zip(ronds, [j for j in range(len(ronds))]))]
    d["obstaclesRectangles"] = [{**{"nom": "obstrect" + str(i)}, **o} for o, i in list(zip(rectangles, [j for j in range(len(rectangles))]))]
    d["robots"] = [{**{"nom": "robot" + str(i)}, **o} for o, i in list(zip(robots, [j for j in range(len(robots))]))]
   
    with open("config/" + args.config, "w") as json_file:
        json_file.write(json.dumps(d, indent=4))

#Fonction pour charger la config
def load():
    """
    Fonction permettant de charger une configuration
    """
    global s_x, s_y, lst_obstacles_rond, lst_obstacles_rect, lst_robots

    with open("config/" + args.config, "r") as json_file:
        data = json.load(json_file)

        lst_obstacles_rect = data["obstaclesRectangles"]
        lst_obstacles_rond = data["obstaclesRonds"]
        lst_robots = data["robots"]
   
#On charge la config passée en paramètres
load()

#Boucle principale
while True:
    #On reset l'ecran
    screen.fill((255,255,255))

    #On affiche les obstacles
    for o in lst_obstacles_rect:
        pygame.draw.rect(screen, COULEUR_OBSTACLES, ((o["posX"] - o["longueur"]/2 + s_x/2) * e, (o["posY"] - o["largeur"]/2 + s_y/2) * e, o["longueur"] * e, o["largeur"] * e))

    for o in lst_obstacles_rond:
        pygame.draw.circle(screen, COULEUR_OBSTACLES, ((o["posX"] + s_x/2) * e, (o["posY"] + s_x/2) * e), o["rayon"] * e)

    for o in lst_robots:
        i = pygame.transform.rotate(img, o["angle"])
        screen.blit(i, ((o["posX"] + s_x/2) * e - i.get_width()/2, (o["posY"] + s_y/2) * e - i.get_height()/2))

    #On update et affiche l'obstacle courant
    x2, y2 = getMouse()
    if pressing and current == "rectangle":
        current_obst = {"posX": (x1 + x2)/2, "posY": (y1 + y2)/2, "longueur": abs(x1 - x2), "largeur": abs(y1 - y2)}
        pygame.draw.rect(screen, COULEUR_OBSTACLES, ((current_obst["posX"] - current_obst["longueur"]/2 + s_x/2) * e, (current_obst["posY"] - current_obst["largeur"]/2 + s_y/2) * e, current_obst["longueur"] * e, current_obst["largeur"] * e))

    elif pressing and current == "cercle":
        current_obst = {"posX": x1, "posY": y1, "rayon": int(sqrt((x2 - x1)**2 + (y2 - y1)**2))}
        pygame.draw.circle(screen, COULEUR_OBSTACLES, ((current_obst["posX"] + s_x/2) * e, (current_obst["posY"] + s_y/2) * e), current_obst["rayon"] * e)

    elif pressing and current == "robot":
        current_obst = {"posX": x1, "posY": y1, "angle": int(sqrt((x2 - x1)**2 + (y2 - y1)**2)%360) * 5 - 90}
        i = pygame.transform.rotate(img, current_obst["angle"])
        screen.blit(i, ((current_obst["posX"] + s_x/2) * e - i.get_width()/2, (current_obst["posY"] + s_y/2) * e - i.get_height()/2))

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
                if current == "rectangle":
                    lst_obstacles_rect.append({"posX": (x1 + x2)/2, "posY": (y1 + y2)/2, "longueur": abs(x1 - x2), "largeur": abs(y1 - y2)})
                elif current == "cercle":
                    lst_obstacles_rond.append({"posX": x1, "posY": y1, "rayon": int(sqrt((x2 - x1)**2 + (y2 - y1)**2))})
                elif current == "robot":
                    lst_robots.append({"posX": x1, "posY": y1, "angle": int(sqrt((x2 - x1)**2 + (y2 - y1)**2)%360 * 5 - 90)})
            pressing = False

        #Clic droit de la souris pour supprimer un élément
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            x, y = getMouse()

            for o in lst_obstacles_rect:
                if o["posX"] - o["longueur"]/2 < x < o["posX"] + o["longueur"]/2 and o["posY"] - o["largeur"]/2 < y < o["posY"] + o["largeur"]/2:
                    lst_obstacles_rect.remove(o)
            for o in lst_obstacles_rond:
                if sqrt((o["posX"] - x)**2 + (o["posY"] - y)**2) < o["rayon"]:  
                    lst_obstacles_rond.remove(o)
            for o in lst_robots:
                if sqrt((o["posX"] - x)**2 + (o["posY"] - y)**2) < 5.85:  
                    lst_robots.remove(o)

        #Raccourci claviers pour sauvegarder/
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                pressing = False
                current = "robot"
            elif event.key == pygame.K_c:
                pressing = False
                current = "cercle"
            elif event.key == pygame.K_b:
                pressing = False
                current = "rectangle"
            elif event.key == pygame.K_s:
                save(lst_robots, lst_obstacles_rect, lst_obstacles_rond, s_x, s_y)
            elif event.key == pygame.K_l:
                load()