import pygame, random
from pygame import *


#Creating Pipe
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (300, random_pipe_pos - 100))
    bottom_pipe = pipe_surface.get_rect(midtop = (300, random_pipe_pos))
    return bottom_pipe, top_pipe

#Moving Pipes
def move_pipes(pipes):
    for i in pipes:
        i.centerx -= 5
    return pipes

#Drwa Pipes
def draw_pipes(pipes):
    for i in pipes:
        if i.bottom >= screen_height:
            screen.blit(pipe_surface,i)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,i)

#Check Collision
def check_collision(pipes):
    for i in pipes:
        if bd_rect.colliderect(i):
            return False
    
    if bd_rect.top <= -5 or bd_rect.bottom >= 450:
        return False
    
    return True

#Check Top


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
gravity = 0.5
bird_movement = 0
pipe_list = []
pipe_height = [200, 250, 300, 350, 400]
game_active = True


SPAWNPIPE = pygame.USEREVENT
 
#Set up Timer
pygame.time.set_timer(SPAWNPIPE,1500)


# Load images
bg_day = pygame.image.load('Flappy Bird/flappy bird/img/bg-day.png')
floor = pygame.image.load('Flappy Bird/flappy bird/img/base.png')
bd_mid = pygame.image.load('Flappy Bird/flappy bird/img/bluebird-midflap.png')
pipe_surface = pygame.image.load('Flappy Bird/flappy bird/img/pipe-green.png')

# Bird rectangle
bd_rect = bd_mid.get_rect(center=(50, 256))

# Game loop
run = True
while run:

    clock.tick(fps)



    # Draw background
    screen.blit(bg_day, (0, 0))
    if game_active:
        #Bird Movement
        bird_movement += gravity
        bd_rect.centery += bird_movement
        # Draw bird
        screen.blit(bd_mid, bd_rect)

        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Draw and scroll floor
    screen.blit(floor, (ground_scroll, 450))
    ground_scroll -= scrool_speed
    if ground_scroll <= -50:
        ground_scroll = 0


   

    #Collision
    game_active = check_collision(pipe_list)


    # Event handling
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 8
            
            if i.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bd_rect.center = (50, 256)
                bird_movement = 0

        if i.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
