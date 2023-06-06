import pygame
import random
import sys
from pygame.locals import *

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

# Images choisies
player_image = pygame.transform.scale(pygame.image.load("V5.6/joueur.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)) # Au cas où l'image fait pas la bonne taille

ball_image = pygame.transform.scale(pygame.image.load("V5.6/balle.png"), (BALL_WIDTH, BALL_HEIGHT)) 

coeur_image = pygame.transform.scale(pygame.image.load("V5.6/coeur.png"), (COEUR_WIDTH, COEUR_HEIGHT)) 
coeurfaded_image = pygame.transform.scale(pygame.image.load("V5.6/coeurfaded.png"), (COEUR_WIDTH, COEUR_HEIGHT)) 

background_image = pygame.transform.scale(pygame.image.load("V5.6/terrain.png"), (WIDTH, HEIGHT))


listex = [110, 230, 350, 470, 590, 110, 230, 350, 470, 590]
listey = [190, 190, 190, 190, 190, 310, 310, 310, 310, 310]

sprites = []  # Liste pour stocker les sprites
sprite_rects = []  # Liste pour stocker les rectangles englobants des sprites
selected_sprite = None # Le sprite choisi

# Charger les 10 sprites
for i in range(10):
    sprite_image = pygame.transform.scale(pygame.image.load(f"V5.6/{i+1}.png"), (SPRITE_WIDTH, SPRITE_HEIGHT))
    sprites.append(sprite_image)
    sprite_rect = sprite_image.get_rect()
    sprite_rect.topleft = (listex[i], listey[i])  # Définir les coordonnées du sprite
    sprite_rects.append(sprite_rect)

# Charger une musique parmis la super compilation
i = random.randint(0, 17)
path = 'V5.6/output_folder/mp3/'
musique = path + str(i) + '.mp3'
pygame.mixer.music.load(musique)



# Définir les dimensions et la position du rectangle pour le score
largeur_rectangle = 150
hauteur_rectangle = 40
x_rectangle = (WIDTH - largeur_rectangle) // 2  # Au milieu horizontalement
y_rectangle = 0  # En haut de l'écran

# Variables du jeu
score = 0
font = pygame.font.Font(None, 36)
dercolsol = 0
nbrotation = 0

# Initialisation de l'écran de jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu V5.6")


def start_screen():
    selected_sprite = None
    screen.fill(BLACK)
    start_text = font.render("Appuyez sur une touche pour commencer", True, WHITE)
    start_text_rect = start_text.get_rect()
    start_text_rect.centerx = WIDTH // 2
    start_text_rect.centery = HEIGHT // 5
    screen.blit(start_text, start_text_rect)
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

                if start_text_rect.collidepoint(mouse_pos):
                    print("L'utilisateur a cliqué sur le texte de départ.")

                for i, sprite_rect in enumerate(sprite_rects):
                    if sprite_rect.collidepoint(mouse_pos):
                        print(f"L'utilisateur a cliqué sur le sprite {i+1}.")
                        selected_sprite = i

        screen.fill(BLACK)  # Effacer l'écran
        screen.blit(start_text, start_text_rect)

        # Dessiner les sprites à l'écran
        for i, sprite in enumerate(sprites):
            screen.blit(sprite, sprite_rects[i])

            # Dessiner le rectangle autour du sprite sélectionné
            if selected_sprite is not None and selected_sprite == i:
                pygame.draw.rect(screen, GRIS, sprite_rects[i], 2)

        pygame.display.flip()

def game(i):
    global score, nbcoeur
    
    if i != 0:
        player_image = pygame.transform.scale(pygame.image.load(f"V5.6/{i+1}.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
    else:
        i = 0
        player_image = pygame.transform.scale(pygame.image.load(f"V5.6/{i+1}.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

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
                    return False
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

def game_over_screen():
    screen.fill(BLACK)
    perdu_text = font.render("Perdu", True, WHITE)
    perdu_text_rect = perdu_text.get_rect()
    perdu_text_rect.centerx = WIDTH // 2
    perdu_text_rect.centery = HEIGHT // 2
    screen.blit(perdu_text, perdu_text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

# Boucle principale
running = True
while running:
    pygame.mixer.music.play()
    selected_sprite = None
    selected_skin = start_screen()
    print('le skin choisi est :', selected_skin)
    score = 0
    nbcoeur = 1
    dercolsol = 0
    nbrotation = 0
    game_over = game(selected_skin)
    print(game_over)
    if game_over == False:
        game_over_screen()
        running = False

pygame.quit()
