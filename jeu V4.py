import pygame
import random
import sys

pygame.init()

# Paramètres de l'écran
WIDTH = 800
HEIGHT = 600

#  Paramètres de couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paramètres de la balle
BALL_WIDTH = 50
BALL_HEIGHT = 50
BALL_RADIUS = 50//2

# Paramètres du joueur
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80

# Paramètres du coeur
COEUR_WIDTH = 75
COEUR_HEIGHT = COEUR_WIDTH*(440/512)
nbcoeur = 1

# Images choisies
player_image = pygame.image.load("V4/joueur.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT)) # Au cas où l'image fait pas la bonne taille

ball_image = pygame.image.load("V4/balle.png")
ball_image = pygame.transform.scale(ball_image, (BALL_WIDTH, BALL_HEIGHT)) 

coeur_image = pygame.image.load("V4/coeur.png")
coeur_image = pygame.transform.scale(coeur_image, (COEUR_WIDTH, COEUR_HEIGHT)) 
coeurfaded_image = pygame.image.load("V4/coeurfaded.png")
coeurfaded_image = pygame.transform.scale(coeurfaded_image, (COEUR_WIDTH, COEUR_HEIGHT)) 

background_image = pygame.image.load("V4/terrain.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Définir les dimensions et la position du rectangle
largeur_rectangle = 150
hauteur_rectangle = 40
x_rectangle = (WIDTH - largeur_rectangle) // 2  # Au milieu horizontalement
y_rectangle = 0  # En haut de l'écran

# Variables du jeu
score = 0
font = pygame.font.Font(None, 36)
dercolsol = 0


# Initialisation de l'écran de jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu V4")


def game():
    global score, nbcoeur
    
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

        # Si la balle touche le sol
        if ball_pos[1] + BALL_RADIUS >= HEIGHT:
            current_time = pygame.time.get_ticks()
            if current_time - dercolsol >= 1000 :
                if nbcoeur >= 1:
                    nbcoeur -= 1  # Décrémenter le nombre de vies
                    dercolsol = current_time
                    ball_velocity_y = -ball_velocity_y

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

        ball_pos[0] += ball_velocity_x

        # Si la balle touche les murs
        if ball_pos[0] <= BALL_RADIUS or ball_pos[0]+BALL_RADIUS//2 >= WIDTH:
            ball_velocity_x = -ball_velocity_x

        # Dessiner les éléments
        screen.blit(background_image, (0, 0)) # Le terrain

        screen.blit(ball_image, (ball_pos[0] - BALL_RADIUS, ball_pos[1] - BALL_RADIUS)) # La balle
        
        screen.blit(player_image, (player_pos[0], player_pos[1])) # Le joueur
        
            # Afficher le nombre de coeur(s)
        if nbcoeur == 1 :
            screen.blit(coeur_image, (25, 25)) # Le coeur
        
        if nbcoeur == 0:
            screen.blit(coeurfaded_image, (25,25)) # Le coeur plus transparent

            # Afficher le score
        pygame.draw.rect(screen, BLACK, (x_rectangle, y_rectangle, largeur_rectangle, hauteur_rectangle))

        text = font.render("Score: " + str(score), True, WHITE)
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
    score = 0
    nbcoeur = 1
    dercolsol = 0
    game_over = game()
    print(game_over)
    if game_over == False:
        game_over_screen()
        running = False

pygame.quit()
