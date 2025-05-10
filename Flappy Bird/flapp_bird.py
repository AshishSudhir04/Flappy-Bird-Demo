import pygame
from pygame import *


#Creating Pipe
#def create_pipe():


# Initialize Pygame
pygame.init()

# Game settings
fps = 30
screen_width = 288
screen_height = 512

# Create game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Set up clock
clock = pygame.time.Clock()

# Load variables
ground_scroll = 0
scrool_speed = 4
gravity = 0.25
bird_movement = 0
pipe_list = []
SPAWNPIPE = pygame.USEREVENT

#Set up Timer
pygame.time.set_timer(SPAWNPIPE,1200)


# Load images
bg_day = pygame.image.load('Flappy Bird/flappy bird/img/bg-day.png')
floor = pygame.image.load('Flappy Bird/flappy bird/img/base.png')

bd_mid = pygame.image.load('Flappy Bird/flappy bird/img/bluebird-midflap.png')
pipes = pygame.image.load('Flappy Bird/flappy bird/img/pipe-green.png')

# Bird rectangle
bd_rect = bd_mid.get_rect(center=(50, 256))

# Game loop
run = True
while run:

    clock.tick(fps)

    # Draw background
    screen.blit(bg_day, (0, 0))

    # Draw and scroll floor
    screen.blit(floor, (ground_scroll, 450))
    ground_scroll -= scrool_speed
    if ground_scroll <= -50:
        ground_scroll = 0


    #Bird Movement
    bird_movement += gravity
    bd_rect.centery += bird_movement



    # Draw bird
    screen.blit(bd_mid, bd_rect)

    # Event handling
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6

        #if i.type == SPAWNPIPE:
            #pipe_list.append(crete_pipe)

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
