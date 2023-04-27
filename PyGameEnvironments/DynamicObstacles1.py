import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set the width and height of the screen [width, height]
WIDTH = 700
HEIGHT = 500

# Initialize Pygame
pygame.init()

# Set the size of the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the caption of the window
pygame.display.set_caption("Dynamic Obstacles")

# Define the class for the moving obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed = -self.speed

# Define the class for the player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

# Create a list of all the sprites
all_sprites_list = pygame.sprite.Group()

# Create a list of the moving obstacles
obstacle_list = pygame.sprite.Group()

# Create the player object
player = Player(50, 50)
all_sprites_list.add(player)

# Create some initial obstacles
for i in range(5):
    x = random.randrange(WIDTH - 30)
    y = random.randrange(HEIGHT - 30)
    speed = random.randrange(1, 5)
    obstacle = Obstacle(x, y, speed)
    all_sprites_list.add(obstacle)
    obstacle_list.add(obstacle)

# Set the clock for the game
clock = pygame.time.Clock()

# Start the game loop
done = False
while not done:
    # --- Event Processing ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game Logic ---
    # Get the mouse position and update the player
    pos = pygame.mouse.get_pos()
    player.update(pos[0], pos[1])

    # Update the moving obstacles
    obstacle_list.update()

    # --- Drawing ---
    # Clear the screen
    screen.fill(BLACK)

    # Draw all the sprites
    all_sprites_list.draw(screen)

    # --- Wrap-up ---
    # Update the screen
    pygame.display.flip()

    # Set the game's frame rate
    clock.tick(60)

# Close the window and quit Pygame
pygame.quit()
