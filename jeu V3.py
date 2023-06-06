import pygame
import random
import sys

pygame.init()

# Paramètres de l'écran
WIDTH = 800
HEIGHT = 600

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paramètres de la balle
BALL_WIDTH = 50
BALL_HEIGHT = 50
BALL_RADIUS = 50//2

# Paramètres du joueur
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80

# Images choisies
player_image = pygame.image.load("V3/joueur.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT)) # Au cas où l'image fait pas la bonne taille
ball_image = pygame.image.load("V3/balle.png")
ball_image = pygame.transform.scale(ball_image, (BALL_WIDTH, BALL_HEIGHT)) # Au cas où l'image fait pas la bonne taille
background_image = pygame.image.load("V3/terrain.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) # Au cas où l'image fait pas la bonne taille

# Variables du jeu
score = 0
font = pygame.font.Font(None, 36)

# Initialisation de l'écran de jeu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu V3")

def game():
    global score
    
    # Position initiale de la balle
    ball_pos = [WIDTH // 2, BALL_RADIUS]
    ball_velocity_y = 0
    ball_velocity_x = 1
    gravity = 0.1

    # Position initiale du joueur
    player_pos = [WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 60]

    clock = pygame.time.Clock()
    running = True

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
            return False

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

        text = font.render("Score: " + str(score), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, 20)
        screen.blit(text, text_rect) # Le text


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
    game_over = game()
    print(game_over)
    if game_over == False:
        game_over_screen()
        running = False

pygame.quit()
