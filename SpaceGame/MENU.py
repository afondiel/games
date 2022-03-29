import pygame               #importation de la bibliothèque pygame
from pygame.locals import * #Importe toutes les fonctions de la classe "locals"    
#oporating system/bibliothèque python qui utilise les fonctions windows...quit();open()
import os


#bibliothèque os faisant appel à la fonction environ qui Centre la fenêtre de jeu/ 
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Initialisation des modules pygame 
pygame.init() 

pygame.display.set_caption("ARCADE CLASSIC")    #Nom de la fenêtre
icon = pygame.image.load('icon.png')            # charger l'image 
pygame.display.set_icon(icon)                   #Définis une icon pour la fenêtre

#taille de la fenêtre du jeu en (x,y)
LARGEUR=800   
HAUTEUR=600

fenêtre=pygame.display.set_mode((LARGEUR, HAUTEUR)) # créer la fenêtre

police="ArcadeClassic.ttf"  #réutilisation d'une police externe du Menu

#CONSTANTES couleurs 
BLANC=(255, 255, 255)
GRIS=(50, 50, 50)
JAUNE=(255, 255, 0)

FOND_ECRAN = pygame.image.load("FOND_ECRAN.jpg") #charger le fond d'écran

# Fonction de rendu de texte 
def texte(message, textFont, textSize, textColor):#définition de la fonction texte recevant des paramètres
    newFont=pygame.font.Font(textFont, textSize)  #variable correspondant à la police et à la taille 
    newText=newFont.render(message, 0, textColor) #formatage du texte  

    return newText #renvoie le texte formaté

#Fonction du menu princiaple du jeu
def MENU():

    menu=True
    selected="JOUER"

    while menu:
        #gestion des evenements
        for event in pygame.event.get(): #récupère tous les évènements
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:     # Utilise flèche du haut
                    selected="JOUER"
                elif event.key==pygame.K_DOWN:  # Utilise flèche du bas
                    selected="QUITER"
                if event.key==pygame.K_RETURN:
                    if selected=="JOUER":
                        os.startfile("JEU.py")            #Lancer le fichier jeu
                        pygame.quit()                     #Puis ferme le menu
                        quit()
                    if selected=="QUITER":
                        pygame.quit()                     #Ferme le menu
                        quit()

        #Design (couleurs + police + fond écran) du menu
        fenêtre.blit(FOND_ECRAN, (0, 0))    #On définit le fond écran du jeu et sa position

        #réutilisation de la fonction "texte" pour le rendu des différentes partie de notre menu
        titredujeu=texte("ARCADE CLASSIC", police, 85, JAUNE)  

        #Formage du texte sectionné au clavier 
        if selected=="JOUER":
            texte_jouer = texte("JOUER", police, 70, BLANC)
        else:
            texte_jouer = texte("JOUER", police, 70, GRIS)
        if selected=="QUITER":
            texte_quitter= texte("QUITER", police, 70, BLANC)
        else:
            texte_quitter = texte("QUITER", police, 70, GRIS)

        #Trouve le rectangle en focntion de la taille de la surface de textes sur l'écran
        titredujeu_rect=titredujeu.get_rect() 
        jouer_rect=texte_jouer.get_rect()
        quitter_rect=texte_quitter.get_rect()
        
        #Définit les positions de nos textes sur la fenêtre de jeu
        fenêtre.blit(titredujeu, (LARGEUR/2 - (titredujeu_rect[2]/2), 50))
        fenêtre.blit(texte_jouer, (LARGEUR/2 - (jouer_rect[2]/2), 300))
        fenêtre.blit(texte_quitter, (LARGEUR/2 - (quitter_rect[2]/2), 400))
        pygame.display.update()   #Mise à jour de la fenêtre

#Appel la fonction du menu
MENU()

