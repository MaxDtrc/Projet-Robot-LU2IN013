import pygame
import os
from os import listdir
from os.path import isfile, join

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


pygame.init()
screen = pygame.display.set_mode((s_x, s_y))

pygame.display.set_caption('Driftator SDK') 
screen.fill((255,255,255))

#Menu des configs
cfg_list = [f for f in listdir("config") if isfile(join("config", f))]
cfg_page = 0
cfg_selected = 0

#Menu des IA
ia_list = [f for f in listdir("demo_ia") if isfile(join("demo_ia", f))]
ia_page = 0
ia_selected = 0

#Menu de la vue
vue_list = ["2D", "3D"]
vue_selected = 0

ctrl = False


def show_menu():
    """
    Fonction affichant le menu latéral
    """
    global screen

    #Affichage du titre
    text = pygame.font.Font('freesansbold.ttf', 50).render("DRIFTATOR EDITOR", False, (0, 0, 0))
    screen.blit(text, (375 - text.get_width()/2, 20))

    #Affichage des menus
    
    for x, y, selected, lst, titre, clr, clr_selected in zip([cfg_menu[0], ia_menu[0], vue_menu[0]], [cfg_menu[1], ia_menu[1], vue_menu[1]], [cfg_selected, ia_selected, vue_selected], [cfg_list, ia_list, vue_list], ["Choix de la config", "Choix de l'IA", "Choix de la vue"], [clr_cfg_cases, clr_ia_cases, clr_vue_cases], [clr_cfg_selected, clr_ia_selected, clr_vue_selected]):
        text = pygame.font.Font('freesansbold.ttf', font_size).render(titre, False, (0, 0, 0))
        screen.blit(text, (x - text.get_width()/2, y - 35 - text.get_height()/2))

        pygame.draw.rect(screen, clr_selected, (x - 2 - w/2, y - 2 + 50 * selected - h/2, w + 4, h + 4), border_radius=6)
        for i in range(min(5, len(lst))):
            pygame.draw.rect(screen, clr, (x - w/2, y + (h+10) * i - h/2, w, h), border_radius=6)

            #Affichage du texte
            text = pygame.font.Font('freesansbold.ttf', font_size).render(lst[i], True, (0, 0, 0))
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

        #Relachement du clic gauche -> On ajoute l'obstacle
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            x, y = pygame.mouse.get_pos()

            #Menu config
            if cfg_menu[0] - w/2 < x < cfg_menu[0] + w/2 and cfg_menu[1] - h/2 < y < cfg_menu[1] + min(5, len(cfg_list)) * (h * 1.1):
                cfg_selected = int((y - cfg_menu[1] + h/2)//((h * 1.2)))
            #Menu IA
            elif ia_menu[0] - w/2 < x < ia_menu[0] + w/2 and ia_menu[1] - h/2 < y < ia_menu[1] + min(5, len(ia_list)) * (h * 1.1):
                ia_selected = int((y - ia_menu[1] + h/2)//((h * 1.2)))
            #Menu des vues
            elif vue_menu[0] - w/2 < x < vue_menu[0] + w/2 and vue_menu[1] - h/2 < y < vue_menu[1] + min(5, len(vue_list)) * (h * 1.1):
                vue_selected = int((y - vue_menu[1] + h/2)//((h * 1.2)))
            #Lancer
            elif p_x - p_w/2 < p_x < p_x + p_w/2 and p_y - p_h/2 < y < p_y:
                #On lance le code
                pygame.display.quit()
                running = False
                os.execv('/usr/bin/python', ['/usr/bin/python', 'main.py', '-c', 'config/' + cfg_list[cfg_selected], '-ia', 'demo_ia/' + ia_list[ia_selected], '-v', str(vue_selected + 1)])
                
        #Clic droit
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and ctrl:
            #Menu config
            if cfg_menu[0] - w/2 < x < cfg_menu[0] + w/2 and cfg_menu[1] - h/2 < y < cfg_menu[1] + min(5, len(cfg_list)) * (h * 1.1):
                cfg_selected = int((y - cfg_menu[1] + h/2)//((h * 1.2)))
                os.execv('/usr/bin/python', ['/usr/bin/python', 'edit_config.py', '-c', cfg_list[cfg_selected]])
        
        #Detection de la touche CTRL
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                ctrl = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrl = False