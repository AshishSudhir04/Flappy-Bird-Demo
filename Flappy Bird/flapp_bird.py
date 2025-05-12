import pygame, random
from pygame import *


#Creating Pipe
def create_rect_for_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (300, random_pipe_pos - 100))
    bottom_pipe = pipe_surface.get_rect(midtop = (300, random_pipe_pos))
    return bottom_pipe, top_pipe

#Moving Pipes
def move_pipes(pipes):
    for i in pipes:
        i.centerx -= 5
    return pipes

#Draw Pipes
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
        if bird_rect.colliderect(i):
            return False
    
    if bird_rect.top <= -5 or bird_rect.bottom >= 450:
        return False
    
    return True

#Rotate Bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

#Animate Bird
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

#Display Score
def display_score(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f"Score: {int(score)} ",True,(255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50) )
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)} ",True,(255, 255, 255))
        score_rect = score_surface.get_rect(center = (144, 50) )
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)} ",True,(255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (144, 412) )
        screen.blit(high_score_surface, high_score_rect)

#Display High_score
def get_high_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency= 44100, size= 16, channels = 1, buffer = 624)

# Initialize Pygame
pygame.init()

# Game settings
fps = 45 
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
score = 0
high_score = 0
collision_happened = False



game_font = pygame.font.Font('Flappy Bird/flappy bird/04B_19__.TTF', 20)

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1500)

BIRDFLAP = pygame.USEREVENT + 1 
pygame.time.set_timer(BIRDFLAP,200)


 


bird_downflap = pygame.image.load('Flappy Bird/flappy bird/img/bluebird-downflap.png')
bird_midflap = pygame.image.load('Flappy Bird/flappy bird/img/bluebird-midflap copy.png')
bird_upflap = pygame.image.load('Flappy Bird/flappy bird/img/bluebird-upflap.png')

bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))



# Load images
bg_day = pygame.image.load('Flappy Bird/flappy bird/img/bg-day.png')
floor = pygame.image.load('Flappy Bird/flappy bird/img/base.png')
#bird_surface = pygame.image.load('Flappy Bird/flappy bird/img/bluebird-midflap.png')
pipe_surface = pygame.image.load('Flappy Bird/flappy bird/img/pipe-green.png')

# Bird rectangle
#bird_rect = bird_surface.get_rect(center=(50, 256))


#game_over_surface
game_over_surface = game_font.render('Press "R" To Restart',True,(255, 255, 255))
game_over_surface_rect = game_over_surface.get_rect(center = (144, 206) )

flap_sound = pygame.mixer.Sound('Flappy Bird/flappy bird/audio/wing.wav')
death_sound = pygame.mixer.Sound('Flappy Bird/flappy bird/audio/hit.wav')
# Game loop
run = True
while run:

    clock.tick(fps)



    # Draw background
    screen.blit(bg_day, (0, 0)) 


    if game_active:
        #Bird Movement
        bird_movement += gravity
        bird_rect.centery += bird_movement

        #rotated Bird
        rotated_bird = rotate_bird(bird_surface)

        # Draw bird
        screen.blit(rotated_bird, bird_rect)

        #Moving the Pipe
        pipe_list = move_pipes(pipe_list)

        #Drawing the Pipe
        draw_pipes(pipe_list)

        score += 0.01
        display_score("main_game")

        # Draw and scroll floor
        screen.blit(floor, (ground_scroll, 450))
        ground_scroll -= scrool_speed
        if ground_scroll <= -50:
            ground_scroll = 0

    
    else:
        
        screen.blit(floor, (ground_scroll, 450))
        high_score = get_high_score(score,high_score)
        display_score("game_over")
        score = 0
        screen.blit(game_over_surface,game_over_surface_rect)





    #Collision
    if game_active:
        game_active = check_collision(pipe_list)
        if not game_active and not collision_happened:
            death_sound.play()
            collision_happened = True


    # Event handling
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False

        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE and game_active == True:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if i.key == pygame.K_r and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                collision_happened = False

        if i.type == SPAWNPIPE:
            pipe_list.extend(create_rect_for_pipe())

        if i.type == BIRDFLAP:
            bird_index = (bird_index + 1) % 3  
            
        bird_surface, bird_rect = bird_animation()

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
