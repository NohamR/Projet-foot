import pygame
import random
import sys
import time

pygame.init()
game_over = False
game_over_time = None

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu V1")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paramètres de la balle
BALL_RADIUS = 30
ball_pos = [WIDTH // 2, BALL_RADIUS]  # Position initiale de la balle

# Paramètres du joueur
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 20
player_pos = [WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 60]  # Position initiale du joueur
player_speed = 10  # Vitesse de déplacement du joueur

# Variables du jeu
clock = pygame.time.Clock()
running = True

ball_velocity_y = 0  # Vélocité verticale initiale
ball_velocity_x = 1  # Vélocité horizontale initiale
gravity = 0.1  # Accélération due à la gravité

score = 0 # Le score au début de la partie
font = pygame.font.Font(None, 36)  # Crée une police pour le texte (taille 36)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des mouvements du joueur
    mouse_pos = pygame.mouse.get_pos()
    player_pos[0] = mouse_pos[0] - PLAYER_WIDTH // 2  # Met à jour la position du joueur en fonction de la position de la souris

    # Mise à jour de la logique du jeu
    
    
    #gravity
    ball_velocity_y += gravity  # Applique l'accélération due à la gravité à la vélocité
    ball_pos[1] += ball_velocity_y  # Met à jour la position verticale de la balle en fonction de la vélocité

    # Si la balle touche le joueur
    if ball_pos[1] + BALL_RADIUS >= player_pos[1] and ball_pos[0] >= player_pos[0] and ball_pos[0] <= player_pos[0] + PLAYER_WIDTH: # Si y'a collision avec le joueur
        ball_pos[1] = player_pos[1] - BALL_RADIUS  # Rétablit la position de la balle au-dessus du joueur
        ball_velocity_y = -ball_velocity_y  # Inverse la vélocité verticale pour simuler le rebond
        score += 1  # Incrémente le score
        ball_velocity_x += random.uniform(-2, 2) # Change la vélocité horizontale de la balle
        print("Score :", score)  # Affiche le score à la console (remplace par ton propre code d'affichage)


    # Si la balle touche le sol
    if ball_pos[1] + BALL_RADIUS >= HEIGHT:
        game_over = True  # Active l'état "game_over"
        ball_pos[1] = HEIGHT + BALL_RADIUS  # Déplace la balle hors de l'écran pour la cacher
        player_pos[1] = HEIGHT + PLAYER_HEIGHT  # Déplace le joueur hors de l'écran pour le cacher
        print('game over')


    elif ball_pos[1] <= BALL_RADIUS:
        ball_pos[1] = BALL_RADIUS  # Rétablit la position de la balle à l'intérieur de l'écran
        ball_velocity_y = -ball_velocity_y  # Inverse la vélocité pour simuler le rebond


    # Partie pour faire en sorte que la balle se déplace de gauche à droite
    # Mise à jour de la logique du jeu
    ball_pos[0] += ball_velocity_x  # Met à jour la position horizontale de la balle en fonction de la vélocité horizontale

    # Vérifie la collision avec les bords gauche et droit de l'écran
    if ball_pos[0] <= BALL_RADIUS or ball_pos[0] >= WIDTH - BALL_RADIUS:
        ball_velocity_x = -ball_velocity_x  # Inverse la vélocité horizontale pour changer la direction de la balle


    # Dessiner les éléments
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, ball_pos, BALL_RADIUS)
    pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], PLAYER_WIDTH, PLAYER_HEIGHT))

    # Le score
    text = font.render("Score: " + str(score), True, WHITE)  # Convertit le score en chaîne de caractères et crée un objet de texte
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, 20)  # Positionne le texte au centre en haut de l'écran
    screen.blit(text, text_rect)  # Affiche le texte sur l'écran

    # Rafraîchissement de l'écran
    pygame.display.flip()
    clock.tick(60)  # Limite le taux de rafraîchissement à 60 FPS

pygame.quit()
