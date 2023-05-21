import pygame
import os
from os import listdir
from os.path import isfile, join
import sys

"""
Variables generales
"""

#Variables couleurs
clr_cfg_cases = (122, 222, 255)
clr_cfg_selected = (31, 73, 87)

clr_ia_cases = (255, 112, 102)
clr_ia_selected = (255, 17, 0)

clr_vue_cases = (145, 255, 162)
clr_vue_selected = (39, 94, 47)

clr_play = (255, 137, 46)

font_size = 16

#Tailles des boutons
h, w = 40, 240

#Positions des menus
cfg_menu = (187, 150)
ia_menu = (583, 150)
vue_menu = (187, 450)

#Bonton lancer
p_x, p_y = 375, 675
p_h, p_w = 60, 100

#Taille de la fenêtre
s_x = 750
s_y = 750


"""
Initialisation du code
"""

def creer_fichier():
            
    global current_title, ia_writing, cfg_writing, ia_list, cfg_list
    if ia_writing:
        if current_title == "":
            ia_writing = False
        else:
            open("demo_ia/" + current_title + ".ia", "w").close()
            ia_list.insert(-1, current_title + ".ia")
            print("Nouveau fichier .ia créé")
            ia_writing, current_title = False, ""
    if cfg_writing:
        if current_title == "":
            ia_writing = False
        else :
            with open("config/" + current_title + ".json", "w") as f:
                f.write("{\"terrain\":{\"tailleX\":152, \"tailleY\":152}, \"obstaclesRonds\":[], \"obstaclesRectangles\":[], \"robots\":[], \"balises\":[]}")
            cfg_list.insert(-1, current_title + ".json")
            print("Nouvelle config créée")
            cfg_writing, current_title = False, ""


pygame.init()
screen = pygame.display.set_mode((s_x, s_y))

pygame.display.set_caption('Driftator SDK') 
screen.fill((255,255,255))

#Menu des configs
cfg_list = [f for f in listdir("config") if isfile(join("config", f))]
cfg_list.append("+")
cfg_page = 0
cfg_selected = 0
cfg_writing = False

#Menu des IA
ia_list = [f for f in listdir("demo_ia") if isfile(join("demo_ia", f))]
ia_list.append("+")
ia_page = 0
ia_selected = 0
ia_writing = False

#Menu de la vue
vue_list = ["2D", "3D"]
vue_selected = 0
vue_writing = False

ctrl = False

current_title = ""

latest_selected = 0

def show_menu():
    """
    Fonction affichant le menu latéral
    """
    global screen

    #Affichage du titre
    text = pygame.font.Font('freesansbold.ttf', 50).render("DRIFTATOR EDITOR", False, (0, 0, 0))
    screen.blit(text, (375 - text.get_width()/2, 20))

    #Affichage des menus
    
    for x, y, page, selected, lst, titre, clr, clr_selected, writing in zip([cfg_menu[0], ia_menu[0], vue_menu[0]], [cfg_menu[1], ia_menu[1], vue_menu[1]], [cfg_page, ia_page, 0], [cfg_selected, ia_selected, vue_selected], [cfg_list, ia_list, vue_list], ["Choix de la config", "Choix de l'IA", "Choix de la vue"], [clr_cfg_cases, clr_ia_cases, clr_vue_cases], [clr_cfg_selected, clr_ia_selected, clr_vue_selected], [cfg_writing, ia_writing, vue_writing]):
        text = pygame.font.Font('freesansbold.ttf', font_size).render(titre, False, (0, 0, 0))
        screen.blit(text, (x - text.get_width()/2, y - 35 - text.get_height()/2))

        pygame.draw.rect(screen, clr_selected, (x - 2 - w/2, y - 2 + 50 * selected - h/2, w + 4, h + 4), border_radius=6)

        #Affichage des pages
        if len(lst) > 5:
            text = pygame.font.Font('freesansbold.ttf', font_size).render(str(page + 1) + "/" + str(len(lst)//5 + 1), False, (0, 0, 0))
            screen.blit(text, (x - text.get_width()/2 + w/2 - 5, y - 35 - text.get_height()/2))

        for i in range(min(5, len(lst) - 5 * page)):
            pygame.draw.rect(screen, clr, (x - w/2, y + (h+10) * i - h/2, w, h), border_radius=6)

            #Affichage du texte
            if i == min(5, len(lst) - 5 * page) - 1 and writing:
                text = pygame.font.Font('freesansbold.ttf', font_size).render(current_title, True, (0, 0, 0))
            else:
                text = pygame.font.Font('freesansbold.ttf', font_size).render(lst[i + 5 * page].split('.')[0], True, (0, 0, 0))

            screen.blit(text, (x + 5 - w/2, y + (h+10) * i - text.get_height()/2))

    #Bouton lancer
    pygame.draw.rect(screen, clr_play, (p_x - p_w/2, p_y - p_h/2, p_w, p_h), border_radius=6)
    text = pygame.font.Font('freesansbold.ttf', font_size).render("Lancer", True, (0, 0, 0))
    screen.blit(text, (p_x - text.get_width()/2, p_y - text.get_height()/2))

"""
Script principal
"""

#Boucle principale
running = True
while running:
    #On reset l'ecran
    screen.fill((255,255,255))

    show_menu()

    #On affiche le fond
    pygame.display.update()

    #On check le clic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            exit() #On arrête.

        #Selection menu
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = pygame.mouse.get_pos()

            creer_fichier()

            #Menu config
            if cfg_menu[0] - w/2 < x < cfg_menu[0] + w/2 and cfg_menu[1] - h/2 < y < cfg_menu[1] + min(5, len(cfg_list)) * (h * 1.1):
                clicked = int((y - cfg_menu[1] + h/2)//((h * 1.2)))
                if clicked == cfg_selected and cfg_selected == len(cfg_list) - 5 * cfg_page - 1:
                    cfg_writing = True
                cfg_selected = clicked if clicked < min(5, len(cfg_list) - 5 * cfg_page) else cfg_selected
                latest_selected = 0
            #Menu IA
            elif ia_menu[0] - w/2 < x < ia_menu[0] + w/2 and ia_menu[1] - h/2 < y < ia_menu[1] + min(5, len(ia_list)) * (h * 1.1):
                clicked = int((y - ia_menu[1] + h/2)//((h * 1.2)))
                if clicked == ia_selected and clicked == len(ia_list) - 5 * ia_page - 1:
                    ia_writing = True
                ia_selected = clicked if clicked < min(5, len(ia_list) - 5 * ia_page) else ia_selected
                latest_selected = 1
            #Menu des vues
            elif vue_menu[0] - w/2 < x < vue_menu[0] + w/2 and vue_menu[1] - h/2 < y < vue_menu[1] + 2 * (h * 1.1):
                vue_selected = int((y - vue_menu[1] + h/2)//((h * 1.2)))
                latest_selected = -1
            #Lancer
            elif p_x - p_w/2 < x < p_x + p_w/2 and p_y - p_h/2 < y < p_y + p_h/2 and cfg_list[cfg_selected + 5 * cfg_page] != "+" and ia_list[ia_selected + 5 * ia_page] != "+":
                #On lance la simulation
                pygame.display.quit()
                running = False
                os.execv(sys.executable, [sys.executable, 'main.py', '-c', 'config/' + cfg_list[cfg_selected + 5 * cfg_page], '-ia', 'demo_ia/' + ia_list[ia_selected + 5 * ia_page], '-v', str(vue_selected + 1)])
                
        #Ctrl Clic
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and ctrl:
            #Menu config
            if cfg_menu[0] - w/2 < x < cfg_menu[0] + w/2 and cfg_menu[1] - h/2 < y < cfg_menu[1] + min(5, len(cfg_list)) * (h * 1.1):
                #Lancement de l'éditeur de config
                cfg_selected = int((y - cfg_menu[1] + h/2)//((h * 1.2)))
                if cfg_list[cfg_selected + 5 * cfg_page] != "+":
                    os.execv(sys.executable, [sys.executable, 'edit_config.py', '-c', cfg_list[cfg_selected + 5 * cfg_page]])
            elif ia_menu[0] - w/2 < x < ia_menu[0] + w/2 and ia_menu[1] - h/2 < y < ia_menu[1] + min(5, len(ia_list)) * (h * 1.1):
                #Ouverture de VSCode
                ia_selected = int((y - ia_menu[1] + h/2)//((h * 1.2)))
                if ia_list[ia_selected + 5 * ia_page] != "+":
                    os.system("code demo_ia/" + ia_list[ia_selected + 5 * ia_page])
        
        #Detection des touches
        elif event.type == pygame.KEYDOWN:
            #Touche controle et écriture d'un nom de fichier
            if event.key == pygame.K_BACKSPACE and len(current_title) != 0:
                current_title = current_title[:-1]
            elif ia_writing or cfg_writing:
                current_title += pygame.key.name(event.key).replace('8', '_') if pygame.key.name(event.key) in "abcdefghijklmnopqrstuvwxyz8" else ""

            if event.key == pygame.K_LCTRL:
                ctrl = True
            #Defilement des pages
            if event.key == pygame.K_LEFT:
                if latest_selected == 0:
                    cfg_page -= 1 if cfg_page > 0 and not cfg_writing else 0
                    cfg_selected = 0
                elif latest_selected == 1:
                    ia_page -= 1 if ia_page > 0 and not ia_writing else 0
                    ia_selected = 0
            if event.key == pygame.K_RIGHT:
                if latest_selected == 0:
                    cfg_page += 1 if (cfg_page + 1) * 5 < len(cfg_list) and not cfg_writing else 0
                    cfg_selected = 0
                elif latest_selected == 1:
                    ia_page += 1 if latest_selected == 1 and (ia_page + 1) * 5 < len(ia_list) and not ia_writing else 0
                    ia_selected = 0
            if event.key == pygame.K_UP:
                cfg_selected -= 1 if latest_selected == 0 and cfg_selected > 0 and not cfg_writing else 0
                ia_selected -= 1 if latest_selected == 1 and ia_selected > 0 and not ia_writing else 0
            if event.key == pygame.K_DOWN:
                cfg_selected += 1 if latest_selected == 0 and cfg_selected < min(4, len(cfg_list) - 5 * cfg_page - 1) and not cfg_writing else 0
                ia_selected += 1 if latest_selected == 1 and ia_selected < min(4, len(ia_list) - 5 * ia_page - 1) and not ia_writing else 0
            if event.key == pygame.K_RETURN:
                creer_fichier()

 
            #Suppression d'un fichier
            if ctrl and event.key == pygame.K_DELETE:
                if latest_selected == 0 and not cfg_writing and cfg_list[cfg_selected + 5 * cfg_page] != '+':
                    os.remove("config/" + cfg_list[cfg_selected + 5 * cfg_page])
                    cfg_list.remove(cfg_list[cfg_selected + 5 * cfg_page])
                if latest_selected == 1 and not ia_writing and ia_list[ia_selected + 5 * ia_page] != '+':
                    os.remove("demo_ia/" + ia_list[ia_selected + 5 * ia_page])
                    ia_list.remove(ia_list[ia_selected + 5 * ia_page])


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrl = False