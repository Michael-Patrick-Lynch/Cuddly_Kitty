# general setup
import pygame, sys
from pygame import *
pygame.init()

# window
DISPLAYSURF = pygame.display.set_mode((1400, 750), 0, 32)
pygame.display.set_caption('Cuddly Kitty')

# time
fpsClock = pygame.time.Clock()
FPS = 60
dog_spawn = USEREVENT + 1
pygame.time.set_timer(dog_spawn, 3000)
boost_over = USEREVENT + 2
boost = False
boosted_already = False
bird_spawn = USEREVENT + 3
pygame.time.set_timer(bird_spawn, 7000)
bird_poo = USEREVENT + 4
pygame.time.set_timer(bird_poo, 1864)
damage_cooldown_over = USEREVENT + 5


# music + sound effects
jumpSound = pygame.mixer.Sound('jump.mp3')
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1, 0.0)
birdpooSound = pygame.mixer.Sound('birdpoo.mp3.flac')

# colours
black = (0, 0 , 0)
white = (255, 255, 255)


# player
playerimg = pygame.transform.scale((pygame.image.load('Cat_orange (1).png')), (100, 100))
player_rect = pygame.Rect(200, 200, 100, 100)
player_gravity = 0

# backround
groundimg = pygame.transform.scale((pygame.image.load('ground.png')), (1400, 150))
ground_rect = pygame.Rect(0, 640, 1400, 200)
skyimg = pygame.transform.scale((pygame.image.load('Sky.png')), (1400, 750))
sky_rect = pygame.Rect(0, 0, 1400, 750)

# dog (enemy) 
dogimg = pygame.transform.scale((pygame.image.load('pitbull_2.0 (1).png')), (150, 150))
dog_rect = pygame.Rect(-200, 550, 150, 150)
dog_speed_multiplier = .5

# bird (enemy)
birdimg = pygame.transform.scale((pygame.image.load('blue_Bird.png')), (150, 150))
bird_rect = pygame.Rect(900, -25, 150, 150)
birdpooimg = pygame.transform.scale(pygame.image.load('bird_poo.png'), (50, 50))
birdpoo_rect = pygame.Rect(900, 400, 50, 50)
birdpoo_gravity = 6

# health
heartimg = pygame.transform.scale(pygame.image.load('heart.png'), (50, 50))
heart_rect = pygame.Rect(40, 690, 50, 50)
heart_rect.center = (125, 710)
player_health = 3
health_text = (f"{player_health}   X")
damage_cooldown_period = False

# text
fontObj = pygame.font.Font('Pixeltype.ttf', 60)
textSurfaceObj = fontObj.render(health_text, True, black)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (50, 710)


while True: # main game loop

    for event in pygame.event.get(): # 1.EVENT HANDLING FOR LOOP
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and on_ground == True:
                player_gravity = -32
                pygame.mixer.Sound.play(jumpSound)

            if event.key == K_SPACE and on_ground == False and boosted_already == False:
                boost = True
                boosted_already = True
                pygame.time.set_timer(boost_over, 80)

        if event.type == MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -30

        if event.type == dog_spawn:
            dog_rect.x = 1600
            dog_rect.bottom = 660
            if dog_speed_multiplier <= 3.5:
                dog_speed_multiplier = dog_speed_multiplier + .33
            else: 
                dog_speed_multiplier = 3.5

        if event.type == bird_spawn:
            bird_rect.x = 1600

        if event.type == bird_poo and (bird_rect.x > 0 and bird_rect.x < 1400):
            birdpoo_rect.top = bird_rect.bottom
            birdpoo_rect.x = bird_rect.x
            pygame.mixer.Sound.play(birdpooSound)

        if event.type == boost_over:
            boost = False

        if event.type == damage_cooldown_over:
            damage_cooldown_period = False

        

    # 2.UPDATING THE GAMESTATE BASED ON THE EVENTS
    player_gravity += 1.5
    player_rect.y += player_gravity
    dog_rect.x -= 10 * dog_speed_multiplier
    bird_rect.x -= 5
    birdpoo_rect.y += birdpoo_gravity
    
    if boost == True:
        player_rect.x += 50

    if player_rect.bottom > 650:
         player_rect.bottom = 650
         on_ground = True
         boosted_already = False
    else:
        on_ground = False

    if player_rect.left < 0: player_rect.left = 0
    if player_rect.right > 1400: player_rect.right = 1400

    if pygame.Rect.colliderect(player_rect, dog_rect) and damage_cooldown_period == False:
        player_health -= 1
        pygame.time.set_timer(damage_cooldown_over, 2000)
        damage_cooldown_period = True
        health_text = (f"{player_health}   X")
        textSurfaceObj = fontObj.render(health_text, True, black)

    if player_health == 0:
        sys.exit()
        pygame.close()
        
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_rect.x += 8
    if keys[pygame.K_LEFT]:
        player_rect.x -= 8


    # 3.UPDATING THE SCREEN TO REFLECT THE NEW GAMESTATE

    DISPLAYSURF.blit(skyimg, sky_rect)
    DISPLAYSURF.blit(groundimg, ground_rect)
    DISPLAYSURF.blit(dogimg, dog_rect)
    DISPLAYSURF.blit(birdimg, bird_rect)
    if birdpoo_rect.y <= 630:
        DISPLAYSURF.blit(birdpooimg, birdpoo_rect)

    DISPLAYSURF.blit(playerimg, player_rect)
    DISPLAYSURF.blit(heartimg, heart_rect)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    

    pygame.display.update()
    fpsClock.tick(FPS)


