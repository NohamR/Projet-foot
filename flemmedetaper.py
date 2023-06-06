# player_image = pygame.image.load("V5/joueur.png")
# player_image = pygame.transform.scale(pygame.image.load("V5/joueur.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)) # Au cas où l'image fait pas la bonne taille

# for i in range (1,11):
#     print('sprite_image_', i, ' = pygame.transform.scale(pygame.image.load("V5.5/', i, '.png"), (SPRITE_WIDTH, SPRITE_HEIGHT))', sep='')


SPRITE_WIDTH = 100  # Largeur d'un sprite
SPRITE_HEIGHT = 100  # Hauteur d'un sprite
SPACING_X = 20  # Espacement horizontal entre les sprites
SPACING_Y = 20  # Espacement vertical entre les lignes de sprites
SCREEN_WIDTH = 800  # Largeur de l'écran
SCREEN_HEIGHT = 600  # Hauteur de l'écran

# Calculer les coordonnées de position des sprites
start_x = (SCREEN_WIDTH - (SPRITE_WIDTH * 5 + SPACING_X * 4)) // 2
start_y = (SCREEN_HEIGHT - (SPRITE_HEIGHT * 2 + SPACING_Y)) // 2
listex = []
listey = []
for row in range(2):
    for col in range(5):
        x = start_x + col * (SPRITE_WIDTH + SPACING_X)
        y = start_y + row * (SPRITE_HEIGHT + SPACING_Y)
        listex.append(x)
        listey.append(y)

print('listex = ', listex, sep='')
print('listey = ' , listey, sep='')