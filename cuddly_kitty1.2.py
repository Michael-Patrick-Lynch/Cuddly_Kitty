# general setup
import pygame, sys
from pygame import *
pygame.mixer.pre_init(44100, -16, 1, 16)
pygame.init()


# window
DISPLAYSURF = pygame.display.set_mode((1400, 750), 0, 32)
pygame.display.set_caption('Cuddly Kitty')

# time
fpsClock = pygame.time.Clock()
FPS = 60

# events
dog_spawn = USEREVENT + 1
boost_over = USEREVENT + 2
bird_spawn = USEREVENT + 3
bird_poo = USEREVENT + 4
damage_cooldown_over = USEREVENT + 5

# sound effects
jumpSound = pygame.mixer.Sound('jump.mp3')
jumpSound.set_volume(.2)
barkSound = pygame.mixer.Sound('dog-growl.mp3')
barkSound.set_volume(8)
poo_splat_on_cats_head_sound = pygame.mixer.Sound('poo_falling.mp3.flac')
meowSound = pygame.mixer.Sound('Meow.ogg')
birdpooSound = pygame.mixer.Sound('birdpoo.mp3.flac')

# colours
black = (0, 0 , 0)
white = (255, 255, 255)
beige = (230, 170, 170)

# player
player_health = 3
player_gravity = 0

# backround
ground_rect = pygame.Rect(0, 640, 1400, 200)
sky_rect = pygame.Rect(0, 0, 1400, 750)

# images
playerimg = pygame.transform.scale((pygame.image.load('Cat_orange (1).png')), (100, 100))
dogimg = pygame.transform.scale((pygame.image.load('pitbull_2.0 (1).png')), (150, 150))
birdimg = pygame.transform.scale((pygame.image.load('blue_Bird.png')), (150, 150))
skyimg = pygame.transform.scale((pygame.image.load('Sky.png')), (1400, 750))
groundimg = pygame.transform.scale((pygame.image.load('ground.png')), (1400, 150))
birdpooimg = pygame.transform.scale(pygame.image.load('bird_poo.png'), (50, 50))
catnipimg = pygame.transform.scale(pygame.image.load('Cat_Nip.png'), (50, 50))


# health
heartimg = pygame.transform.scale(pygame.image.load('heart.png'), (50, 50))
heart_rect = pygame.Rect(40, 690, 50, 50)
heart_rect.center = (125, 710)
health_text = (f"{player_health}   X")

# text
fontObj = pygame.font.Font('Pixeltype.ttf', 60)
textSurfaceObj = fontObj.render(health_text, True, black)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (50, 710)

highscore = 0
birdpoo_gravity = 6

# sound objects and eveents don't need to be brought in using the global keyword

def main():
    global fpsClock, DISPLAYSURF, FPS
    
    showStartScreen()
    while True:
        rungame()
        showGameOverScreen()
        
# rungame() means a new game is starting so we must set all the vairables to the right levels
# we must also tell the python interpreter that we are talking about the global variables
def rungame():

    global player_health, player_gravity, on_ground, boosted_already, boost, damage_cooldown_period
    global player_rect, dog_rect, bird_rect, birdpoo_rect, dog_speed_multiplier
    global highscore, score, player_flickering, catnip_on_screen

    setGame() # resets the game state to how it should be at the start of a game

    while True: # main game loop

        for event in pygame.event.get(): # 1.EVENT HANDLING FOR LOOP
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_UP and on_ground == True:
                    pygame.mixer.Sound.play(jumpSound)
                    player_gravity = -32
                    

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
                player_flickering = 'ON'

            

        # 2.UPDATING THE GAMESTATE BASED ON THE EVENTS

        # gravity and enemy movement
        player_gravity += 1.5
        player_rect.y += player_gravity
        birdpoo_rect.y += birdpoo_gravity
        dog_rect.x -= 10 * dog_speed_multiplier
        bird_rect.x -= 5
        
        # player movement, collisions
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
            player_damaged()
            pygame.mixer.Sound.play(barkSound)
        
        if pygame.Rect.colliderect(player_rect, birdpoo_rect) and damage_cooldown_period == False:
            player_damaged()
            pygame.mixer.Sound.play(poo_splat_on_cats_head_sound)

        if pygame.Rect.colliderect(player_rect, catnip_rect):
            player_health += 1
            catnip_on_screen = False
            catnip_rect.x -= 300

        if player_health == 0:
            return
            
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player_rect.x += 8
        if keys[pygame.K_LEFT]:
            player_rect.x -= 8


        # 3.UPDATING THE SCREEN TO REFLECT THE NEW GAMESTATE

        score += 1
        formatted_score = (f'CURRENT SCORE: {score}')
        scoretxtSurf = fontObj.render(formatted_score, True, black)
        scoretxt_rect = scoretxtSurf.get_rect()
        scoretxt_rect.center = (400, 715)
        health_text = (f"{player_health}   X")
        textSurfaceObj = fontObj.render(health_text, True, black)


       


        if score > highscore:
            highscore = score


        DISPLAYSURF.blit(skyimg, sky_rect)
        DISPLAYSURF.blit(groundimg, ground_rect)
        DISPLAYSURF.blit(dogimg, dog_rect)
        DISPLAYSURF.blit(birdimg, bird_rect)
        DISPLAYSURF.blit(heartimg, heart_rect)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        DISPLAYSURF.blit(scoretxtSurf, scoretxt_rect)

        if catnip_on_screen:
            DISPLAYSURF.blit(catnipimg, catnip_rect)

        if birdpoo_rect.y <= 630:
            DISPLAYSURF.blit(birdpooimg, birdpoo_rect)

        if damage_cooldown_period == False:
            DISPLAYSURF.blit(playerimg, player_rect)
        elif damage_cooldown_period == True and player_flickering == 'ON':
            player_flickering = 'OFF'
            DISPLAYSURF.blit(playerimg, player_rect)
        elif player_flickering == 'OFF':
            player_flickering = 'ON'
       
        pygame.display.update()
        fpsClock.tick(FPS)



def player_damaged():
    global player_health, damage_cooldown_period, textSurfaceObj
    player_health -= 1
    pygame.time.set_timer(damage_cooldown_over, 2000)
    damage_cooldown_period = True
    health_text = (f"{player_health}   X")
    textSurfaceObj = fontObj.render(health_text, True, black)
    meowSound.play()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress(): # returns the first key pressed. unless esc or quit are selected then it terminates the app
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showGameOverScreen():
    global highscore

    pygame.mixer.music.load('No Hope.mp3')
    pygame.mixer.music.play(-1, 0.0)
    gameOverFont = pygame.font.Font('Pixeltype.ttf', 200)
    gameTxtSurf = gameOverFont.render('Game', True, white)
    overTxtSurf = gameOverFont.render('Over', True, white)
    gameTxt_rect = gameTxtSurf.get_rect()
    overTxt_rect = overTxtSurf.get_rect()
    gameTxt_rect.center = (700, 325)
    overTxt_rect.center = (708, 435)

    instructionsFont = pygame.font.Font('Pixeltype.ttf', 50)
    instructions_to_continue = "Press Any Key to Start a New Game"
    instructionsSurf = instructionsFont.render(instructions_to_continue, True, white)
    instructions_rect = instructionsSurf.get_rect()
    instructions_rect.center = (700, 625)

    highscore_formatted = (f'HIGHSCORE: {highscore}')
    highscoreSurf = instructionsFont.render(highscore_formatted, True, white)
    highscore_rect = highscoreSurf.get_rect()
    highscore_rect.center = (700, 200)


    DISPLAYSURF.fill(black)
    DISPLAYSURF.blit(gameTxtSurf, gameTxt_rect)
    DISPLAYSURF.blit(overTxtSurf, overTxt_rect)
    DISPLAYSURF.blit(instructionsSurf, instructions_rect)
    DISPLAYSURF.blit(highscoreSurf, highscore_rect)
    pygame.display.update()
    pygame.time.wait(1500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return


def showStartScreen():

    pygame.mixer.music.load('Cat Song.mp3')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(.2)

    caticonimg = pygame.transform.scale((pygame.image.load('Cat_orange (1).png')), (450, 450))
    caticon_rect = pygame.Rect(550, 200, 450, 450)
    caticon_rect.center = (700, 300)

    instructionsFont = pygame.font.Font('Pixeltype.ttf', 50)
    instructions_to_continue = "Press Any Key to Start a New Game"
    instructionsSurf = instructionsFont.render(instructions_to_continue, True, white)
    instructions_rect = instructionsSurf.get_rect()
    instructions_rect.center = (700, 625)

    while True:
        DISPLAYSURF.fill(beige)
        DISPLAYSURF.blit(caticonimg, caticon_rect)
        
        DISPLAYSURF.blit(instructionsSurf, instructions_rect)

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        fpsClock.tick(FPS)


def setGame():
    global player_health, player_gravity, on_ground, boosted_already, boost, damage_cooldown_period
    global player_rect, dog_rect, bird_rect, birdpoo_rect, catnip_rect, dog_speed_multiplier
    global highscore, score, player_flickering, catnip_on_screen


    # resetting the score and all player variables
    score = 0
    player_health = 3
    damage_cooldown_period = False
    player_flickering = 'ON'
    boost = False
    boosted_already = False

    catnip_on_screen = True

    # playing the game music
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(.1)


    # resetting position of sprites and dog speed multiplier
    player_rect = pygame.Rect(200, 200, 100, 100)
    dog_rect = pygame.Rect(-200, 550, 150, 150)
    bird_rect = pygame.Rect(-400, -25, 150, 150)
    birdpoo_rect = pygame.Rect(-400, 400, 50, 50)
    catnip_rect = pygame.Rect(800, 200, 50, 50)
    dog_speed_multiplier = .5


    # resetting timers
    pygame.time.set_timer(dog_spawn, 3000)
    pygame.time.set_timer(bird_spawn, 7000)
    pygame.time.set_timer(bird_poo, 1864)

if __name__ == '__main__':
    main()