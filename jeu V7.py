import pygame
import random
import sys
from pygame.locals import *
import csv
from math import *
import os

pygame.init()

# Paramètres de l'écran
WIDTH = 800
HEIGHT = 600

#  Paramètres de couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRIS = (111, 111, 111) # pas sûr de la valeur mdrr

# Paramètres de la balle
BALL_WIDTH = 50
BALL_HEIGHT = 50
BALL_RADIUS = 50//2

# Paramètres du joueur
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80

# Paramètres des sprites
SPRITE_WIDTH = 80
SPRITE_HEIGHT = 80

# Paramètres du coeur
COEUR_WIDTH = 75
COEUR_HEIGHT = COEUR_WIDTH*(440/512)
nbcoeur = 1

# Paramètre du smiley
SMILEY_WIDTH = 150
SMILEY_HEIGHT = SMILEY_WIDTH

# Images choisies
player_image = pygame.transform.scale(pygame.image.load("assets/joueur.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)) # Au cas où l'image fait pas la bonne taille

ball_image = pygame.transform.scale(pygame.image.load("assets/balle.png"), (BALL_WIDTH, BALL_HEIGHT)) 

coeur_image = pygame.transform.scale(pygame.image.load("assets/coeur.png"), (COEUR_WIDTH, COEUR_HEIGHT)) 
coeurfaded_image = pygame.transform.scale(pygame.image.load("assets/coeurfaded.png"), (COEUR_WIDTH, COEUR_HEIGHT)) 

smiley_image = pygame.transform.scale(pygame.image.load("assets/smiley.png"), (SMILEY_WIDTH, SMILEY_HEIGHT)) 

background_image = pygame.transform.scale(pygame.image.load("assets/terrain.png"), (WIDTH, HEIGHT))

pygame.display.set_icon(ball_image)

listex = [110, 230, 350, 470, 590, 110, 230, 350, 470, 590]
listey = [190, 190, 190, 190, 190, 310, 310, 310, 310, 310]

sprites = []  # Liste pour stocker les sprites
sprite_rects = []  # Liste pour stocker les rectangles englobants des sprites
selected_sprite = None # Le sprite choisi

# Charger les 10 sprites
for i in range(10):
    sprite_image = pygame.transform.scale(pygame.image.load(f"assets/{i+1}.png"), (SPRITE_WIDTH, SPRITE_HEIGHT))
    sprites.append(sprite_image)
    sprite_rect = sprite_image.get_rect()
    sprite_rect.topleft = (listex[i], listey[i])  # Définir les coordonnées du sprite
    sprite_rects.append(sprite_rect)

# Charger une musique parmis la super compilation
i = random.randint(0, 16)
path = 'assets/mp3/'
musique = path + str(i) + '.mp3'
pygame.mixer.music.load(musique)



# Définir les dimensions et la position du rectangle pour le score
largeur_rectangle = 150
hauteur_rectangle = 40
x_rectangle = (WIDTH - largeur_rectangle) // 2  # Au milieu horizontalement
y_rectangle = 0  # En haut de l'écran

# Charge les scores précédents
def openuseragents(file: str):
    with open(file, newline='') as csvfile:
        return [row for row in csv.DictReader(csvfile, delimiter=';')][0]
stats = openuseragents('assets/.logs.csv')

# Variables du jeu
score = 0
font = pygame.font.Font(None, 36)
dercolsol = 0
nbrotation = 0
rotate = 0
# Initialisation de l'écran de jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projet-foot V7")


def start_screen():
    selected_sprite = None
    screen.fill(BLACK)

    for i, sprite in enumerate(sprites):
        screen.blit(sprite, sprite_rects[i])
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return selected_sprite
            
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche de la souris
                # print("L'utilisateur a cliqué")
                mouse_pos = pygame.mouse.get_pos()

                for i, sprite_rect in enumerate(sprite_rects):
                    if sprite_rect.collidepoint(mouse_pos):
                        print(f"L'utilisateur a cliqué sur le sprite {i+1}.")
                        selected_sprite = i

        screen.fill(BLACK)  # Effacer l'écran

        # Dessiner les sprites à l'écran
        for i, sprite in enumerate(sprites):
            screen.blit(sprite, sprite_rects[i])

            # Dessiner le rectangle autour du sprite sélectionné
            if selected_sprite is not None and selected_sprite == i:
                pygame.draw.rect(screen, GRIS, sprite_rects[i], 2)
            
            texte = "Choisissez le skin de votre choix avec la souris\nAppuyer sur n'importe quelle touche pour commencer la partie\nBonne chance !"
            lignes = texte.split("\n")  # Diviser le texte en lignes
            y = 50  # Position y initiale du texte

            for ligne in lignes:
                y += 30  # Augmenter la position y pour la prochaine ligne

                text = font.render(ligne, True, WHITE)
                text_rect = text.get_rect()
                text_rect.center = (WIDTH // 2, y)
                screen.blit(text, text_rect) # Le score

        pygame.display.flip()

def game(i):
    global score, nbcoeur
    
    if i != None:
        player_image = pygame.transform.scale(pygame.image.load(f"assets/{i+1}.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
    else:
        i = 0
        player_image = pygame.transform.scale(pygame.image.load(f"assets/{i+1}.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

    # Position initiale de la balle
    ball_pos = [WIDTH // 2, BALL_RADIUS]
    ball_velocity_y = 0
    ball_velocity_x = 1
    gravity = 0.1

    # Position initiale du joueur
    player_pos = [WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 60]

    nbcoeur = 1
    clock = pygame.time.Clock()
    running = True
    dercolsol = 0
    nbrotation = 0
    rotate = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Gestion des mouvements du joueur
        mouse_pos = pygame.mouse.get_pos()
        player_pos[0] = mouse_pos[0] - PLAYER_WIDTH // 2

        # Mise à jour de la logique du jeu
        ball_velocity_y += gravity
        ball_pos[1] += ball_velocity_y

        # Si la balle touche le joueur
        if ball_pos[1] + BALL_RADIUS >= player_pos[1] and ball_pos[0] >= player_pos[0] and ball_pos[0] <= player_pos[0] + PLAYER_WIDTH:
            ball_pos[1] = player_pos[1] - BALL_RADIUS
            ball_velocity_y = -ball_velocity_y
            score += 1
            
            # gravity+=score//10
            if score%5  == 0:
                if score//5<=4:
                    print('add gravity + :' , (score//5)/10)
                    gravity += (score//5)/10
                else:print('la gravité est déjà au max')

            ball_velocity_x += random.uniform(-3, 3)
            print("Score :", score)
            nbrotation+=5

        # Si la balle touche le sol
        if ball_pos[1] + BALL_RADIUS >= HEIGHT:
            current_time = pygame.time.get_ticks()
            if current_time - dercolsol >= 1000 :
                if nbcoeur >= 1:
                    nbcoeur -= 1  # Décrémenter le nombre de vies
                    dercolsol = current_time
                    ball_velocity_y = -ball_velocity_y
                    nbrotation+=5


                else:
                    print(nbcoeur)
                    return (False, score)
                    pass
            
            if current_time - dercolsol <= 1000:
                print(nbcoeur)
            
            else:
                nbcoeur = nbcoeur
                print(nbcoeur)

        # Si la balle touche le plafond
        elif ball_pos[1] <= BALL_RADIUS:
            ball_pos[1] = BALL_RADIUS
            ball_velocity_y = -ball_velocity_y
            nbrotation+=5

        ball_pos[0] += ball_velocity_x

        # Si la balle touche les murs
        if ball_pos[0] <= BALL_RADIUS or ball_pos[0]+BALL_RADIUS//2 >= WIDTH:
            ball_velocity_x = -ball_velocity_x
            nbrotation+=5

        # Dessiner les éléments
        screen.blit(background_image, (0, 0)) # Le terrain

        nbrotation+=1
        screen.blit(pygame.transform.rotate(ball_image, nbrotation), (ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS)) # La balle
        
        screen.blit(player_image, (player_pos[0], player_pos[1])) # Le joueur
        
            # Afficher le nombre de coeur(s)
        if nbcoeur == 1 :
            screen.blit(coeur_image, (25, 25)) # Le coeur
        
        if nbcoeur == 0:
            screen.blit(coeurfaded_image, (25,25)) # Le coeur plus transparent

            # Afficher le score
        pygame.draw.rect(screen, BLACK, (x_rectangle, y_rectangle, largeur_rectangle, hauteur_rectangle))

        text = font.render("Score : " + str(score), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 20)
        screen.blit(text, text_rect) # Le score

        #_____________ Ne rien mettre en dessous _____________
        pygame.display.flip()
        clock.tick(60)

def game_over_screen(score):
    screen.fill(BLACK)
    # perdu_text = font.render("Perdu", True, WHITE)
    # perdu_text_rect = perdu_text.get_rect()
    # perdu_text_rect.centerx = WIDTH // 2
    # perdu_text_rect.centery = HEIGHT // 5
    # screen.blit(perdu_text, perdu_text_rect)

    screen.blit(smiley_image, ((WIDTH // 2)-SMILEY_WIDTH/2, (HEIGHT // 2)-SPRITE_HEIGHT/2)) # Le smiley

    moy = float(stats['moy'])
    nbparties = float()

    dec = (( moy * nbparties ) + score) / (nbparties + 1)
    moy = floor(100 * dec ) / 100

    texte = "Perdu\n Votre score était de : " + str(score) + "\n Le score moyen est de : " + str(moy) + '\n Votre meilleur score était de : ' + str(stats['best'])
    lignes = texte.split("\n")  # Diviser le texte en lignes
    y = 50  # Position y initiale du texte
    print(stats)
    for ligne in lignes:
        y += 30  # Augmenter la position y pour la prochaine ligne

        text = font.render(ligne, True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, y)
        screen.blit(text, text_rect) # Le score
    if score >= int(stats['best']):
        best = score
    else:
        best = stats['best']

    l1 = 'score;moy;best;nbparties'
    l2 = str(str(score) + ';' + str(moy) + ';' +  str(best) + ';' + str((int(stats['nbparties'])+1)))

    try:
        os.remove('assets/.logs.csv')
        with open('assets/.logs.csv', "a") as f:
                    f.write(l1 + '\n' + l2 + '\n')
    except Exception as e:
        print(e)

    pygame.display.flip()
    pygame.time.wait(3000)


def replay_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Partie terminée", True, WHITE)
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.centerx = WIDTH // 2
    game_over_text_rect.centery = HEIGHT // 5
    screen.blit(game_over_text, game_over_text_rect)

    replay_button = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
    pygame.draw.rect(screen, WHITE, replay_button)
    replay_text = font.render("Rejouer", True, BLACK)
    replay_text_rect = replay_text.get_rect()
    replay_text_rect.center = replay_button.center
    screen.blit(replay_text, replay_text_rect)

    change_skin_button = pygame.Rect(WIDTH // 2 - 125, 350, 250, 50)
    pygame.draw.rect(screen, WHITE, change_skin_button)
    change_skin_text = font.render("Changer de skin", True, BLACK)
    change_skin_text_rect = change_skin_text.get_rect()
    change_skin_text_rect.center = change_skin_button.center
    screen.blit(change_skin_text, change_skin_text_rect)

    quit_button = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)
    pygame.draw.rect(screen, WHITE, quit_button)
    quit_text = font.render("Quitter", True, BLACK)
    quit_text_rect = quit_text.get_rect()
    quit_text_rect.center = quit_button.center
    screen.blit(quit_text, quit_text_rect)


    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if replay_button.collidepoint(mouse_pos):
                    return
                if change_skin_button.collidepoint(mouse_pos):
                    return False
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                
# Boucle principale
running = True
selected = False
change = None
while running:
    pygame.mixer.music.play()
    selected_sprite = None
    if not selected:
        selected_skin = start_screen()
        selected = True
    print('le skin choisi est :', selected_skin)
    score = 0
    nbcoeur = 1
    dercolsol = 0
    nbrotation = 0
    game_over = game(selected_skin)
    print(game_over)
    if game_over[0] == False:
        game_over_screen(game_over[1])
        change = replay_screen()
        print(change)
        if change == False:
            selected = False
        else : pass

pygame.quit()
