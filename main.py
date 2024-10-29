import pygame
import random
import math
from pygame import mixer

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize pygame window
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# load background image
backround_img = "assets/background.jpg"
background = pygame.image.load(backround_img)

# Loading laser bullet
laser_bullet = pygame.image.load("assets/laserbulletblue24x24.png")

# Background music
mixer.init()
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("assets/spaceship.png")
pygame.display.set_icon(icon)

# Player 
player_img = pygame.image.load("assets/battleship.png")
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0

# Enemy
invader_img = []
invader_x = []
invader_y = []
invader_x_change = []
invader_y_change = []
num_of_invaders = 6

for invader in range(num_of_invaders):
    invader_img.append(pygame.image.load("assets/invader.png"))
    invader_x.append(random.randrange(0, 735))
    invader_y.append(random.randrange(0, 150))
    invader_x_change.append(0.5)
    invader_y_change.append(40)

# Laser bullet
laser_bullet_x = 0
laser_bullet_y = 480
laser_bullet_x_change = 0
laser_bullet_y_change = 1
laser_bullet_state = "ready" # Ready -> laser bullet is invisible
                             # Fire -> Laser bullet is moving

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# Game Over text
game_over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (WHITE))
    screen.blit(score, (x, y))

def game_over_text(x, y):
    game_over_txt = game_over_font.render("GAME OVER!", True, (RED))
    screen.blit(game_over_txt, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(invader_img[invader], (x, y))

def fire_laser_bullet(x, y):
    global laser_bullet_state
    laser_bullet_state = "fire"
    screen.blit(laser_bullet, (x + 20, y + 10))

def check_collision(invader_x, invader_y, laser_bullet_x, laser_bullet_y):
    distance = math.sqrt((math.pow(invader_x - laser_bullet_x, 2)) + (math.pow(invader_y - laser_bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False
    

# Game Loop
running = True
while running:

    # Fill the screen with white color
    screen.fill(BLACK)

    # Inserting background image
    screen.blit(background, (0, 0))

    # # Inserting laser bullet into game window
    # screen.blit(laser_bullet, (laser_bullet_x, laser_bullet_y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= 0.5
            if event.key == pygame.K_RIGHT:
                player_x_change += 0.5
            # Checking for keystroke to fire laser bullet
            if event.key == pygame.K_SPACE:
                if laser_bullet_state == "ready":
                    # Add laser shooting sound
                    laser_bullet_sound = mixer.Sound("laser.wav")
                    laser_bullet_sound.play()
                    # Get cuurent x-axis coordinate of the spaceship
                    laser_bullet_x = player_x
                    fire_laser_bullet(laser_bullet_x, laser_bullet_y)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0




    player_x += player_x_change
    # Draw the player
    player(player_x, player_y)

    # Adding boundaries to the game (player)
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy movement
    for invader in range(num_of_invaders):

        # Game Over
        if invader_y[invader] > 400:
            for invaders in range(num_of_invaders):
                invader_y[invaders] = 2000
            game_over_text(200, 250)
            break

        invader_x[invader] += invader_x_change[invader]
        # Boundaries for the enemy (invader)
        if invader_x[invader] <= 0:
            invader_x_change[invader] = 0.5
            invader_y[invader] += invader_y_change[invader]
        elif invader_x[invader] >= 736:
            invader_x_change[invader] = -0.5
            invader_y[invader] += invader_y_change[invader]
        
        # Collision
        collision = check_collision(invader_x[invader], invader_y[invader], laser_bullet_x, laser_bullet_y)
        if collision:
            # Add explosion sound for invader elimination
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            laser_bullet_y = 480
            laser_bullet_state = "ready"
            score_value += 1
            invader_x[invader] = random.randrange(0, 735)
            invader_y[invader] = random.randrange(0, 150)
        
        enemy(invader_x[invader], invader_y[invader], invader)

    # Bullet movement
    if laser_bullet_state == "fire":
        fire_laser_bullet(laser_bullet_x, laser_bullet_y)
        laser_bullet_y -= laser_bullet_y_change

    # Multiple laser bullet shooting without waiting till laser_bullet_y is 0
    if laser_bullet_y <= 0:
        laser_bullet_y = 480
        laser_bullet_state = "ready"

    show_score(text_x, text_y)

    # Update the screen after any change
    pygame.display.update()

pygame.quit()