import sys
import pygame
import os
pygame.font.init()
pygame.mixer.init()

#general settings
WIDTH, HEIGHT = 900,500 #define resolution
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #open window
WIN_HEIGHT = WIN.get_height()
pygame.display.set_caption('Ouh Pinaise v0.1') #title
ICON = pygame.image.load(os.path.join('assets', 'icon.png')) #icon
pygame.display.set_icon(ICON)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLACK_RED = (180,0,0)

HEALTH_FONT = pygame.font.SysFont('Verdana', 30)
START_FONT = pygame.font.SysFont('Verdana', 20)
WINNER_FONT = pygame.font.SysFont('Verdana', 50)

#middle border
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
TEST = START_FONT.render("Press SPACE to start", 1, WHITE)

#sounds library
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'fire.mp3'))
WINNING_SOUND = pygame.mixer.Sound(os.path.join('assets', 'win.mp3'))
LOOSE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'loose.mp3'))
AMB = pygame.mixer.Sound(os.path.join('assets', 'ost.mp3'))
INTRO = pygame.mixer.Sound(os.path.join('assets', 'wow.mp3'))
DOH = pygame.mixer.Sound(os.path.join('assets', 'doh.mp3'))
CHEERS = pygame.mixer.Sound(os.path.join('assets', 'cheers.mp3'))

#game settings
FPS = 60 
FPS_INTRO = 15
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
STUNNED_TIME = 500 #ms

#normal homer dimension
HOMER_WIDTH, HOMER_HEIGHT = 75,75

#hit homer dimension
HOMER_HIT_W, HOMER_HIT_H = 58, 72

HOMER_WIN_W, HOMER_WIN_H = 262, 286 # x1.09
BEER_WIDTH, BEER_HEIGHT = 20, 64 # x3.2

HOMER_LEFT_HIT = pygame.USEREVENT + 1 # pygame.USEREVENT is a random num, so var is a unique id
HOMER_RIGHT_HIT = pygame.USEREVENT + 2

#images or "surfaces"
HOMER_RIGHT_IMG = pygame.transform.flip(pygame.image.load(os.path.join('assets', 'homer.png')), True, False)
HOMER_LEFT_IMG = pygame.image.load(os.path.join('assets', 'homer.png'))
BEER_BULLET_IMG = pygame.image.load(os.path.join('assets', 'duff.png'))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background3.jpg')), (WIDTH,HEIGHT))
HOMER_HIT = pygame.image.load(os.path.join('assets', 'homerhit.png'))

RIGHT_WIN = pygame.image.load(os.path.join('assets', 'win.png'))
LEFT_WIN = pygame.transform.flip(pygame.image.load(os.path.join('assets', 'win.png')), True, False)
LEFT_LOOSE = pygame.image.load(os.path.join('assets', 'loose.png'))
RIGHT_LOOSE = pygame.transform.flip(pygame.image.load(os.path.join('assets', 'loose.png')), True, False)
LOGO = pygame.image.load(os.path.join('assets', 'logo.png'))

#  112 degrees for right player
# 292 degrees for left player

#rescale/rotate img
HOMER_RIGHT = pygame.transform.scale(HOMER_RIGHT_IMG, (HOMER_WIDTH, HOMER_HEIGHT))
HOMER_LEFT = pygame.transform.scale(HOMER_LEFT_IMG, (HOMER_WIDTH, HOMER_HEIGHT))
HOMER_RIGHT_DOH = pygame.transform.scale(HOMER_HIT, (HOMER_HIT_W,HOMER_HIT_H))
HOMER_LEFT_DOH = pygame.transform.flip(pygame.transform.scale(HOMER_HIT, (HOMER_HIT_W,HOMER_HIT_H)), True, False)
BEER_BULLET = pygame.transform.rotate(pygame.transform.scale(BEER_BULLET_IMG, (BEER_WIDTH, BEER_HEIGHT)), 90)
BEER_BULLET_OPP = pygame.transform.rotate(pygame.transform.scale(BEER_BULLET_IMG, (BEER_WIDTH, BEER_HEIGHT)), -90)

###########################################################################################################

#pip Pillow for image modules
from PIL import Image, ImageSequence

#loading GIF function
def loadGIF(filename):
    pilImage = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(pilImage):
        frame = frame.convert('RGBA')
        pygameImage = pygame.image.fromstring(
            frame.tobytes(), frame.size, frame.mode).convert_alpha()
        frames.append(pygameImage)
        # print(len(frames))
    return frames

#gif animation function and movement
class AnimatedSpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, bottom, images):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom = (x, bottom))
        self.image_index = 0
    def update(self):
        self.image_index += 1
        self.image = self.images[self.image_index % len(self.images)]
        self.rect.x -= 0
        if self.rect.right < 0:
            self.rect.left = pygame.display.get_surface().get_width()

#sprites creation for menu gif
#call function to load
gifFrameList = loadGIF('assets/33.gif')
#create movement and/or animation
animated_sprite = AnimatedSpriteObject(WIN.get_width() // 2, WIN_HEIGHT, gifFrameList)  
#compile sprites in one variable  
MENU_SPRITES = pygame.sprite.Group(animated_sprite)

def draw_window(rh_position, lh_position, rh_bullets, lh_bullets, rh_health, lh_health, RHLIFE, LHLIFE, rhittime, lhittime):
    # WIN.fill(WHITE)
    WIN.blit(BACKGROUND, (0,0))
    pygame.draw.rect(WIN, BLACK_RED, BORDER)
    #health text
    rh_health_text = HEALTH_FONT.render("Health: " + str(rh_health), 1, WHITE)
    lh_health_text = HEALTH_FONT.render("Health: " + str(lh_health), 1, WHITE)
    now = pygame.time.get_ticks()
    #health bar
    #pygame.draw.rect(WIN, (200,0,0), (margin right - bar length, margin top, bar length, height), border, radius)
    pygame.draw.rect(WIN, (200,0,0), (900 - (25 * rh_health), 19, (25 * rh_health), 36), 0, 5)
    pygame.draw.rect(WIN, (200,0,0), (0, 19, (25 * lh_health), 36),0 ,5)
    #health bar > background
    pygame.draw.rect(WIN, (140,0,0), (900 - (25 * RHLIFE), 19, (25 * RHLIFE), 36), 4, 5)
    pygame.draw.rect(WIN, (140,0,0), (0, 19, (25 * LHLIFE), 36), 4, 5)
 
    #display health text
    WIN.blit(rh_health_text, (WIDTH - rh_health_text.get_width() - 10, 17))
    WIN.blit(lh_health_text, (10, 17))

    #display characters
    if now > rhittime:
        WIN.blit(HOMER_RIGHT, (rh_position.x,rh_position.y))
    else:
        WIN.blit(HOMER_RIGHT_DOH, (rh_position.x,rh_position.y))
        ShockPosition(WIN, rh_position.x, rh_position.y)
    
    if now > lhittime:
        WIN.blit(HOMER_LEFT, (lh_position.x,lh_position.y))
    else:
        WIN.blit(HOMER_LEFT_DOH, (lh_position.x,lh_position.y))
        ShockPosition(WIN, lh_position.x + HOMER_HIT_W, lh_position.y)

    #bullets
    for bullet in rh_bullets:
        # pygame.draw.rect(WIN, RED, bullet)
        WIN.blit(BEER_BULLET, bullet)
    
    for bullet in lh_bullets:
        # pygame.draw.rect(WIN, RED, bullet)
        WIN.blit(BEER_BULLET_OPP, bullet)
    #update windows every milliseconds
    pygame.display.update()

#keys movement
def player_one_handle_movement(keys_pressed, lh_position):
            # lh_position.x += 1        
    if keys_pressed[pygame.K_a] and lh_position.x - VEL > 0: #left
        lh_position.x -= VEL
    if keys_pressed[pygame.K_d] and lh_position.x + VEL < BORDER.x - lh_position.width: #right
        lh_position.x += VEL
    if keys_pressed[pygame.K_w] and lh_position.y - VEL > 0: #up
        lh_position.y -= VEL
    if keys_pressed[pygame.K_s] and lh_position.y + VEL < HEIGHT - lh_position.height: #down
        lh_position.y += VEL

def player_two_handle_movement(keys_pressed, rh_position):
    
    if keys_pressed[pygame.K_LEFT] and rh_position.x - VEL > BORDER.x + BORDER.width: #left
        rh_position.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and rh_position.x + VEL < WIDTH - rh_position.width: #right
        rh_position.x += VEL
    if keys_pressed[pygame.K_UP] and rh_position.y - VEL > 0: #up
        rh_position.y -= VEL
    if keys_pressed[pygame.K_DOWN] and rh_position.y + VEL < HEIGHT - rh_position.height: #down
        rh_position.y += VEL

#moving the bullets, removing off screen bullets and collision with character
def handle_beer_bullets(lh_bullets, rh_bullets, lh_position, rh_position):
    for bullet in lh_bullets:
        bullet.x += BULLET_VEL
        if rh_position.colliderect(bullet):
            pygame.event.post(pygame.event.Event(HOMER_RIGHT_HIT))
            lh_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            lh_bullets.remove(bullet)

    for bullet in rh_bullets:
        bullet.x -= BULLET_VEL
        if lh_position.colliderect(bullet):
            pygame.event.post(pygame.event.Event(HOMER_LEFT_HIT))
            rh_bullets.remove(bullet)
        elif bullet.x < 0:
            rh_bullets.remove(bullet)

#render "Winner", appoint looser and winner, play sounds
def showWinner(winner_text, w):
    final_text = WINNER_FONT.render(winner_text, 1, WHITE)
    if (w == 0): #right wins
        WINNING_SOUND.play()
        WIN.blit(final_text, (WIDTH/2 - final_text.get_width()/2, HEIGHT/3 - final_text.get_height()))
        WIN.blit(RIGHT_WIN, (WIDTH/6 - final_text.get_width()/2, HEIGHT/2 - final_text.get_height()))
        WIN.blit(LEFT_LOOSE, (WIDTH/1.30 - final_text.get_width()/2, HEIGHT/2 - final_text.get_height()))
        LOOSE_SOUND.play()
    elif (w == 1): #left wins
        WINNING_SOUND.play()
        WIN.blit(final_text, (WIDTH/2 - final_text.get_width()/2, HEIGHT/3 - final_text.get_height()))
        WIN.blit(LEFT_WIN, (WIDTH/1.30 - final_text.get_width()/2, HEIGHT/2 - final_text.get_height()))
        WIN.blit(RIGHT_LOOSE, (WIDTH/12- final_text.get_width(), HEIGHT/2 - final_text.get_height()))
        LOOSE_SOUND.play()
    pygame.display.update()
    pygame.time.delay(5000)

#show MENU GIF functions
def image_draw(surface):
    MENU_SPRITES.update()
    MENU_SPRITES.draw(surface)
    pygame.display.flip()

def ShockPosition(surface, position_x, position_y):
    STARS = loadGIF('assets/shock.gif')
    animated_stars = AnimatedSpriteObject(position_x,position_y, STARS)
    STARS_SPRITES = pygame.sprite.Group(animated_stars)
    STARS_SPRITES.update()
    STARS_SPRITES.draw(surface)
    pygame.display.flip()

#intro menu
def intro():
    # pygame.time.wait(8000)
    clock = pygame.time.Clock()
    INTRO.play()
    CHEERS.play()
    #logo
    WIN.blit(LOGO, (35, 20))
    
    #instruction text
    start_text = START_FONT.render("Press SPACE to start", 1, WHITE)
    WIN.blit(start_text, (250, 125))
    intro = True #define boolean to keep window opened
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #if SPACE, game starts
                if event.key == pygame.K_SPACE:
                    BULLET_FIRE_SOUND.play()
                    intro = False
        image_draw(WIN) #show img
        clock.tick(15) #FPS

#game
def main():
    #all main game loops (all functions calling here)
    #set char position
    rh_position = pygame.Rect(700, 300, HOMER_WIDTH, HOMER_HEIGHT)
    lh_position = pygame.Rect(100, 300, HOMER_WIDTH, HOMER_HEIGHT)

    #bullets counter
    rh_bullets = [] 
    lh_bullets = [] 
    rhittime = 0
    lhittime = 0

    #total given health
    RHLIFE = 10
    LHLIFE = 10
    rh_health = RHLIFE
    lh_health = LHLIFE
    clock = pygame.time.Clock()
    run = True #define boolean to keep window opened
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
            #fire consequence
                if event.key == pygame.K_LCTRL and len(lh_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(lh_position.x + lh_position.width, lh_position.y + lh_position.height//2 - 2, 13, 42) # 10, 5 is pixels of duff beer
                    lh_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(rh_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(rh_position.x, rh_position.y + rh_position.height//2 - 2, 10, 5) # 10, 5 is pixels of duff beer
                    rh_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # hits consequence        
            if event.type == HOMER_RIGHT_HIT:
                rh_health -= 1
                BULLET_HIT_SOUND.play()
                DOH.play()
                rhittime = pygame.time.get_ticks() + STUNNED_TIME

            if event.type == HOMER_LEFT_HIT:
                lh_health -= 1
                BULLET_HIT_SOUND.play()
                DOH.play()
                lhittime = pygame.time.get_ticks() + STUNNED_TIME

        #winner checking
        winner_text = ""
        if rh_health <= 0:
            winner_text = "Winner !"
            draw_window(rh_position, lh_position, rh_bullets, lh_bullets, rh_health, lh_health, RHLIFE, LHLIFE, rhittime, lhittime)
            w = 0

        if lh_health <= 0:
            winner_text = "Winner !"
            draw_window(rh_position, lh_position, rh_bullets, lh_bullets, rh_health, lh_health, RHLIFE, LHLIFE, rhittime, lhittime)
            w = 1 #left wins

        if winner_text != "":
            showWinner(winner_text, w)
            break #game window shut

        # print(lh_bullets, rh_bullets)

        #functions looping
        
        keys_pressed = pygame.key.get_pressed()
        player_one_handle_movement(keys_pressed, lh_position)
        player_two_handle_movement(keys_pressed, rh_position)

        handle_beer_bullets(lh_bullets, rh_bullets, lh_position, rh_position)
        draw_window(rh_position, lh_position, rh_bullets, lh_bullets, rh_health, lh_health, RHLIFE, LHLIFE, rhittime, lhittime)
    main()

if __name__ == '__main__':
    AMB.play(2)
    intro()
    main()