#Importation des modules
import pygame                         
import random           #Génération des nombres aléatoires
import sys              #Ce modules founit accès à des variables/fonctions utilisé et maintenues par l'interpreteur python (ex : sys.exit(), sys.argv() ... )
from pygame import *
import os               #oporating system/bibliothèque python qui utilise les fonctions windows...quit();open()       


os.environ['SDL_VIDEO_CENTERED'] = '1'    #Centre fenêtre au milieu de l'écran 

#Initialisation des modules
pygame.init()
mixer.init()
pygame.font.init()

volume = pygame.mixer.music.get_volume() #Retourne la valeur du volume, entre 0 et 1
pygame.mixer.music.set_volume(0.1)       #Met le volume à 0.1 

pygame.display.set_caption('ARCADE CLASSIC') #Titre de la fenêtre
pygame.mixer.music.load("MUSIQUE.mp3")       #Charge la musique du jeu
mixer.music.play()                           #Lance la musique

#Taille de la fenêtre du jeu
LARGEUR = 800
HAUTEUR = 600
fenêtre = pygame.display.set_mode((800, 600))

#Icon du jeu
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Position et taille des ennemies et du joueur
taille_joueur = 50
position_joueur = [LARGEUR/2, HAUTEUR-2*taille_joueur]

taille_enemie = 50
position_enemie = [random.randint(0,LARGEUR-taille_enemie), 0]
liste_enemies = [position_enemie]

#Initialisation des Variables
VITESSE = 0
score = 0

font = pygame.font.Font("ArcadeClassic.ttf", 37)  #Définis la police d'écriture  

#Couleurs code RGB 
BLANC =(255, 255, 255)
GRIS =(50, 50, 50)
ROUGE = (255,0,0)
BLEU = (0,0,255)
JAUNE = (255,255,0)

#Charge fond écran + son de fin de partie
FOND_ECRAN = pygame.image.load("FOND_ECRAN.jpg")
son_fin = pygame.mixer.Sound("PERDU.wav")

temps = pygame.time.Clock()   #Permet de définir un système d'horloge

game_over = False

#fonction permettant augmenter de la vitesse en fonction du score    
def niveaux(score, VITESSE):
	if score < 20:
		VITESSE = 5
	elif score < 40:
		VITESSE = 10
	elif score < 60:
		VITESSE = 15
	else:
		VITESSE = 20
	return VITESSE

#la fonction "apparition_enemies" permet de créer de façon aléatoire une listes d'enemies
def apparition_enemies(liste_enemies):      #réçoit la liste d'enimies  
	delai = random.random()             #la variable delai permet valeur entre 0 et 1, 1 exclus.
	if len(liste_enemies) < 10 and delai < 0.1: #génération des 10 éléments avec un delai supérieur à 0.1
		x_pos = random.randint(0,HAUTEUR-taille_enemie) #
		y_pos = 0 #On ne s'interesse pas  à la position en Y car les enemies tombent du haut vers le bas
		liste_enemies.append([x_pos, y_pos]) #Remplissage de la positions de chaque enemie
		
#Affichage de la listes d'énemies 
def afficher_enemies(liste_enemies): #réçoit la liste d'enimies  
	for position_enemie in liste_enemies:
                #affiche chaque enemie sur l'ecran en fonction de sa position d(x,y,taille1,taille2) 
		pygame.draw.rect(fenêtre, BLEU, (position_enemie[0], position_enemie[1], taille_enemie, taille_enemie))

#coloration des enemies
def text_objects(text, font):
    Msg_fin = font.render(text, True, ROUGE)
    return Msg_fin, Msg_fin.get_rect()

#création du bouton de fin de jeu
def bouton(msg, x, y, largeur, longueur, coul1, coul2, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + largeur > mouse[0] > x and y + longueur > mouse[1] > y:         #Souris sur bouton
        pygame.draw.rect(fenêtre, coul2, (x, y, largeur, longueur))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(fenêtre, coul1, (x, y, largeur, longueur))        #Souris pas sur bouton
    TexteBouton = pygame.font.Font("ArcadeClassic.ttf", 20)
    textSurf, textRect = text_objects(msg, TexteBouton)
    textRect.center = ((x + (largeur / 2)), (y + (longueur / 2)))
    fenêtre.blit(textSurf, textRect)

#Fonction permettant de gérer le crash
def crash():
    pygame.mixer.Sound.play(son_fin) #Lance le son de fin de partie
    pygame.mixer.music.stop()        #Et coupe la musique du jeu
    ArcadeClassic = pygame.font.Font("ArcadeClassic.ttf", 117)
    TextSurf, TextRect = text_objects("Perdu !", ArcadeClassic)
    TextRect.center = ((LARGEUR / 2), (HAUTEUR / 2))
    fenêtre.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        bouton("Rejouer", 150, 450, 100, 50, BLANC, GRIS, relancer)
        bouton("Quitter", 550, 450, 100, 50, BLANC, GRIS, quitter)

        pygame.display.update()  #Actualise la fenêtre en entière
        
        temps.tick(30)  #Permet de limiter le nombre d'images par seconde à 30
        
#fonction permettant de relancer le jeu
def relancer():
    pygame.quit()
    os.startfile("JEU.py")
    
#fonction permettant de quitter le jeu  
def quitter():
    pygame.quit()
    quit()
    
#Fonction permettant de determiner la position d'enemies.      
def position_enemies_score(liste_enemies, score):#reçoit la liste d'enemie et le score=0
	for x, position_enemie in enumerate(liste_enemies): # boucler quelque chose et d'avoir un compteur automatique
		if position_enemie[1] >= 0 and position_enemie[1] < HAUTEUR:#centre le bloc enemie sur la surface de l'écran
			position_enemie[1] += VITESSE #augmente la vitesse
		else:
			liste_enemies.pop(x)    #pop () supprime et retourne le dernier objet ou obj de la liste
			score += 1              #increment le compter de score
	return score                            #Le but de return est comme dit, de renvoyer une information à la fin de l’exécution de ta fonction.


#Fonction permettant de gérer la collision d'enemies
def collision(liste_enemies, position_joueur): #réçoit la liste d'enimies et la position du joueur  
	for position_enemie in liste_enemies:  #pour chaque enemie dans la liste
		if detecteur_collision(position_enemie, position_joueur): #Renvoie "Vrai" Si une collision a été detecter 
			return True
	return False

#Fonction permettant de détecter la collision des objets
def detecteur_collision(position_joueur, position_enemie): #reçoit la liste pos joueur et pos enemie
	p_x = position_joueur[0] #position du joueur en x
	p_y = position_joueur[1] #position du joueur en y

	e_x = position_enemie[0] #position de l'enemie en x
	e_y = position_enemie[1] #position de l'enemie en y

	if (e_x >= p_x and e_x < (p_x + taille_joueur)) or (p_x >= e_x and p_x < (e_x+taille_enemie)): #Mise à l'echelle en x
		if (e_y >= p_y and e_y < (p_y + taille_joueur)) or (p_y >= e_y and p_y < (e_y+taille_enemie)): ##Mise à l'echelle en y
			return True #Renvoie "Vrai" / Vérifié
	return False

#boule principale de fin jeu
while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:

			x = position_joueur[0]
			y = position_joueur[1]

			if event.key == pygame.K_LEFT:
				x -= taille_joueur
			elif event.key == pygame.K_RIGHT:
				x += taille_joueur

			position_joueur = [x,y]

	fenêtre.blit(FOND_ECRAN, (0, 0))

	apparition_enemies(liste_enemies)
	
	score = position_enemies_score(liste_enemies, score)
	
	VITESSE = niveaux(score, VITESSE)

	text = "Score " + str(score)
	label = font.render(text, 1, JAUNE)
	fenêtre.blit(label, (LARGEUR-200, HAUTEUR-40))

	if collision(liste_enemies, position_joueur):
		game_over = True
		crash()
	    
	afficher_enemies(liste_enemies)

	pygame.draw.rect(fenêtre, ROUGE, (position_joueur[0], position_joueur[1], taille_joueur, taille_joueur))  

	temps.tick(30)

	pygame.display.update()
