# -*- coding: utf-8 -*-
# By Daniel Petri and Michail - 2012

import pygame, pygame._view, sys, os, random, math
from pygame.locals import *
if not pygame.font:
    print('Warning, fonts disabled!')
if not pygame.mixer:
    print('Warning, sound disabled!')

#Sprites, sounds and backgrounds
w = 'data/sprites/water.jpeg' #Background
w2 = 'data/sprites/tropical_water.jpeg' #Tropical Background
sub_image = 'data/sprites/sub_r.png' #Submarine
sub_crushed1 = 'data/sprites/sub_crashed.png' #Crashed Submarine
sonar1 = 'data/sprites/sonar.png' #Sonar
gem1 = 'data/sprites/gem.png' #Gem
upgrade_menu1 = 'data/sprites/upgrade_menu.png' #Upgrade menu
upgrade_menu22 = 'data/sprites/upgrade_menu2.png' #Second page
full_chest1 = 'data/sprites/full_chest.png' #Chest found (full)
empty_chest1 = 'data/sprites/empty_chest.png' #Empty icon
i = 'data/sprites/iceberg.png' #Iceberg
i2 = 'data/sprites/tropical_island.png'
whale1 = 'data/sprites/whale.png'

pygame.init() #Starts PyGame
ice_crash = pygame.mixer.Sound('data/sounds/ice_crash.ogg') #Crash sound
splash = pygame.mixer.Sound('data/sounds/splash.ogg') #Water splash sound
cash = pygame.mixer.Sound('data/sounds/cash.ogg') #Cash sound
musicPlaying = True
lessRare = False
paused = False

#upgrades
upgrades = False
foundChest = False
longerDiving = False
diveBeneath = False

full = None

class Player(object):
    def __init__(self, x, y, movex, movey, gas, oxy, img, money, sonar_amount):
        self.x=x
        self.y=y
        self.movex=x
        self.movey=y
        self.gas=gas
        self.oxy=oxy
        self.img=img
        self.money = money
        self.sonar_amount = sonar_amount
        self.crushed=False
        self.diving=False
        self.foundChest=False
        self.relative_rectangles=[pygame.Rect(19, 4, 5, 56),
                                pygame.Rect(19, 8, 10, 48),
                                pygame.Rect(19, 10, 15, 44),
                                pygame.Rect(8, 14, 44, 36),
                                pygame.Rect(4, 17, 52, 30),
                                pygame.Rect(2, 20, 56, 24),]
        self.current_rectangles=list(self.relative_rectangles)
    def move(self):
        if self.movex==-2 and self.movey==-2:
            self.img=sub_dia1
            self.relative_rectangles=[pygame.Rect(12, 12, 32, 32),
                                    pygame.Rect(18, 18, 32, 32),
                                    pygame.Rect(24, 24, 32, 32),]
        if self.movex==-2 and self.movey==0:
            self.img=sub_left
            self.relative_rectangles=[pygame.Rect(40, 4, 5, 56),
                                    pygame.Rect(35, 8, 10, 48),
                                    pygame.Rect(30, 10, 15, 44),
                                    pygame.Rect(12, 14, 44, 36),
                                    pygame.Rect(8, 17, 52, 30),
                                    pygame.Rect(6, 20, 56, 24),]
        if self.movex==-2 and self.movey==2:
            self.img=sub_dia4
            self.relative_rectangles=[pygame.Rect(10, 22, 32, 32),
                                    pygame.Rect(16, 16, 32, 32),
                                    pygame.Rect(22, 10, 32, 32),]
        if self.movex==0 and self.movey==-2:
            self.img=sub_up
            self.relative_rectangles=[pygame.Rect(4, 40, 56, 5),
                                    pygame.Rect(8, 35, 48, 10),
                                    pygame.Rect(10, 30, 44, 15),
                                    pygame.Rect(14, 12, 36, 44),
                                    pygame.Rect(17, 8, 30, 52),
                                    pygame.Rect(20, 6, 24, 56),]
        if self.movex==0 and self.movey==2:
            self.img=sub_down
            self.relative_rectangles=[pygame.Rect(4, 19, 56, 5),
                                    pygame.Rect(8, 19, 48, 10),
                                    pygame.Rect(10, 19, 44, 15),
                                    pygame.Rect(14, 8, 36, 44),
                                    pygame.Rect(17, 4, 30, 52),
                                    pygame.Rect(20, 2, 24, 56),]
        if self.movex==2 and self.movey==-2:
            self.img=sub_dia2
            self.relative_rectangles=[pygame.Rect(12, 24, 32, 32),
                                    pygame.Rect(18, 18, 32, 32),
                                    pygame.Rect(24, 12, 32, 32),]
        if self.movex==2 and self.movey==0:
            self.img=sub_right
            self.relative_rectangles=[pygame.Rect(19, 4, 5, 56),
                                    pygame.Rect(19, 8, 10, 48),
                                    pygame.Rect(19, 10, 15, 44),
                                    pygame.Rect(8, 14, 44, 36),
                                    pygame.Rect(4, 17, 52, 30),
                                    pygame.Rect(2, 20, 56, 24),]
        if self.movex==2 and self.movey==2:
            self.img=sub_dia3
            self.relative_rectangles=[pygame.Rect(10, 10, 32, 32),
                                    pygame.Rect(16, 16, 32, 32),
                                    pygame.Rect(22, 22, 32, 32),]

        self.x += self.movex
        self.y += self.movey
        if self.x > (WIDTH - 64): #Boundaries
            self.x = WIDTH - 64
        elif self.x < 0:
            self.x = 0
        if self.y > (HEIGHT - 64):
            self.y = HEIGHT - 64
        elif self.y < 0:
            self.y = 0

        self.oxy-=0.01
        if self.movex or self.movey:
            self.gas-=0.04

        if self.gas<=0 or self.oxy<=0:
            self.crushed=True

        self.current_rectangles=list(self.relative_rectangles)
        for i in range(len(self.current_rectangles)):
            self.current_rectangles[i]=self.relative_rectangles[i].move(self.x, self.y)

class Iceberg(object):
    def __init__(self, x, y, img):
        self.x=x
        self.y=y
        self.img=img
        self.time=0
        self.relative_rectangles=[pygame.Rect(10, 100, 250, 65),
                        pygame.Rect(70, 34, 50, 225),
                        pygame.Rect(27, 70, 245, 74),
                        pygame.Rect(42, 60, 205, 186),
                        pygame.Rect(76, 27, 40, 236),
                        pygame.Rect(20, 80, 270, 50),
                        pygame.Rect(15, 87, 150, 89),
                        pygame.Rect(28, 175, 263, 58),
                        pygame.Rect(35, 165, 245, 76),
                        pygame.Rect(54, 159, 213, 94),
                        pygame.Rect(125, 240, 123, 20),
                        pygame.Rect(97, 250, 133, 16),
                        pygame.Rect(106, 250, 110, 19),
                        pygame.Rect(132, 250, 65, 22),
                        pygame.Rect(65, 41, 64, 25),
                        pygame.Rect(58, 49, 84, 25),]
        self.current_rectangles=list(self.relative_rectangles)
        for i in range(len(self.relative_rectangles)):
            self.current_rectangles[i]=self.relative_rectangles[i].move(self.x, self.y)
    def move(self):
        self.time+=1
        if self.time>=150:
                self.time=0
                self.x+=random.randint(-1, 1)
                self.y+=random.randint(-1, 1)
                self.current_rectangles=list(self.relative_rectangles)
                for i in range(len(self.relative_rectangles)):
                    self.current_rectangles[i]=self.relative_rectangles[i].move(self.x, self.y)

class Whale(object):
    def __init__(self, x,y, img):
        self.x=x
        self.y=y
        self.img=img
        self.relative_rectangles=[pygame.Rect(27, 15, 70, 210), pygame.Rect(5, 70, 115, 50)]
        self.current_rectangles=list(self.relative_rectangles)
        for w in range(len(self.relative_rectangles)):
            self.current_rectangles[w]=self.relative_rectangles[w].move(self.x, self.y)

class Sonar(object):
    def __init__(self, x, y, chests):
        self.x=x  #x and y are the coordinates of the center of sonar
        self.y=y
        self.check_distance(chests)
    def check_distance(self, chests): #tests the distance to the nearest chest
        self.distance=1000
        for chest in chests:
            distance=math.sqrt((self.x-(chest.x+20))**2+(self.y-(chest.y+20))**2) #this +20 is beacause we need the distance to the center of chest
            if distance<self.distance:
                self.distance=distance
        distance=self.distance #Next few lines are to determine the sonar color
        r=0
        g=255
        if distance>255:
            distance-=255
            r+=255
        else:
            r+=distance
            distance-=r
        if distance>255:
            g-=255
            r-=255
        else:
            g-=distance
            r-=distance
        self.color=(r, g, 0)            

class Chest(object):
    def __init__(self, full, gems):
        self.full=full
        self.gems=gems
        self.img=img
        self.relative_rectangles=[pygame.Rect(10, 0, 20, 40),
                                pygame.Rect(0, 10, 40, 20)]
        self.current_rectangles=list(self.relative_rectangles)
        self.move()
    def move(self):
        self.x=random.randint(0, 760)
        self.y=random.randint(0, 460)
        for i in range(len(self.relative_rectangles)):
            self.current_rectangles[i]=self.relative_rectangles[i].move(self.x, self.y)

#Setup
WIDTH = 800
HEIGHT = 500
WHITE = (255,255,255) #Colors
BLACK = (0,0,0)
RED = (192,0,0)
YELLOW = (238,201,0)
FULLSCREENMODE = False
DIVINGTIMER = 100
BIOMETYPE = random.randint(1,4)
orbFont = pygame.font.Font('data/fonts/orbitron_black.ttf',20) #Font variable
screen = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32)
pygame.display.set_caption('Treasure Hunt - 0.7')
clock = pygame.time.Clock()
if BIOMETYPE == 1:
    bg = pygame.image.load(w).convert() #Water
    ice = pygame.image.load(i).convert_alpha() #Original Iceberg
elif BIOMETYPE == 2:
    bg = pygame.image.load(w2).convert() #Dark Water
    ice = pygame.image.load(i).convert_alpha() #Original Iceberg
elif BIOMETYPE == 3:
    bg = pygame.image.load(w).convert() #Water
    ice = pygame.image.load(i2).convert_alpha() #Tropical Island
elif BIOMETYPE == 4:
    bg = pygame.image.load(w2).convert() #Dark Water
    ice = pygame.image.load(i2).convert_alpha() #Tropical Island
sonar = pygame.image.load(sonar1).convert_alpha()
sonar_display = pygame.image.load(sonar1).convert_alpha()
gem = pygame.image.load(gem1).convert_alpha() #Gem sprite
upgrade_menu = pygame.image.load(upgrade_menu1) #Upgrade menu
upgrade_menu2 = pygame.image.load(upgrade_menu22)
full_chest = pygame.image.load(full_chest1).convert_alpha() #Full Chest
empty_chest = pygame.image.load(empty_chest1) #Empty icon
whaleImg = pygame.image.load(whale1).convert_alpha() #whale image
upgradePage = 1 #Upgrade page
sub = pygame.image.load(sub_image).convert_alpha() #Submarines
sub_crushed = pygame.image.load(sub_crushed1).convert_alpha()
sub_left = pygame.transform.rotate(sub,(180.0))
sub_up = pygame.transform.rotate(sub,(90.0))
sub_down = pygame.transform.rotate(sub,(-90.0))
sub_right = pygame.transform.rotate(sub,(0.0))
sub_dia1 = pygame.transform.rotate(sub,(-225.0)) #Diagonal submarines
sub_dia2 = pygame.transform.rotate(sub,(45.0))
sub_dia3 = pygame.transform.rotate(sub,(-45.0))
sub_dia4 = pygame.transform.rotate(sub,(225.0))

for img in (sub_dia1, sub_dia2, sub_dia3, sub_dia4):
    img.scroll(-12, -12)

player=Player(0, 0, 0, 0, 100, 100, sub, 100, 5)
iceberg=Iceberg(random.randint(300,500)-100, random.randint(188,313)-100, ice)
chests=[]
sonars=[]
img_chest = full_chest

if random.randint(1,4) == 1:
    whale = Whale(random.randint(0,120), random.randint(500,750), whaleImg)
elif random.randint(1,4) == 2:
    whale = Whale(random.randint(655,750), random.randint(1000,1250), whaleImg)
elif random.randint(1,4) == 3:
    whale = Whale(random.randint(0,120), random.randint(1500,1750), whaleImg)
else:
    whale = Whale(random.randint(655,750), random.randint(2000,2250), whaleImg)

def add_chest():
    if lessRare == False:
        if random.randint(1, 10)>3:
            full=True
            gems=random.randint(10, 50)
        else:
            full=False
            gems=0
    if lessRare == True:
        if random.randint(1, 10)>=3:
            full=True
            gems=random.randint(10, 50)
        else:
            full=False
            gems=0
    chest=Chest(full, gems)
    collision=True  
    while collision:
        collision=False
        for r1 in chest.current_rectangles:
            for r2 in iceberg.current_rectangles:
                if r1.colliderect(r2):
                    collision=True                          
                    chest.move()
                    break
    chests.append(chest)

def add_sonar():
    if player.sonar_amount>0:
        player.sonar_amount-=1
        sonars.append(Sonar(player.x+32, player.y+32, chests))

for i in range(1):
    add_chest()

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def check_iceberg_collision():
    if diveBeneath == False:
        for r1 in player.current_rectangles:
            for r2 in iceberg.current_rectangles:
                if r1.colliderect(r2):
                    player.img=sub_crushed
                    player.x-=30
                    player.crushed = True
    elif diveBeneath == True and not player.diving:
        for r1 in player.current_rectangles:
            for r2 in iceberg.current_rectangles:
                if r1.colliderect(r2):
                    player.img=sub_crushed
                    player.x-=30
                    player.crushed = True
                
def check_chests_collision():
    for chest in chests:
        for r1 in player.current_rectangles:
            for r2 in chest.current_rectangles:
                if r1.colliderect(r2):
                    return chest

def check_whalePlayer_collision():
    for r1 in whale.current_rectangles:
        for r3 in player.current_rectangles:
            if r1.colliderect(r3):
                player.img=sub_crushed
                player.crushed = True              

def moveWhale():
    if whale.y > -232:
        screen.blit(whale.img, (whale.x, whale.y))
        if not paused and not player.crushed and not upgrades and player.foundChest == False:
            whale.y-=0.8
            check_whalePlayer_collision()
    for w in range(len(whale.relative_rectangles)):
        whale.current_rectangles[w]=whale.relative_rectangles[w].move(whale.x, whale.y)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            player.foundChest=False #Any key removes chest found menu
            if event.key == K_ESCAPE:
                if not upgrades:
                    pygame.quit()
                    sys.exit()
                else:
                    upgrades = not upgrades
            elif event.key == ord('a'):
                player.movex = -2
            elif event.key == ord('d'):
                player.movex = +2
            elif event.key == ord('w'):
                player.movey = -2
            elif event.key == ord('s'):
                player.movey = +2
            elif event.key == ord('m'):
                musicPlaying = not musicPlaying
            elif event.key == ord('p'):
                paused = not paused
            elif event.key == ord('e'):
                if not paused and not player.crushed and not player.diving:
                    upgrades = not upgrades
            elif event.key == ord('f'):
                player.crushed = False
                player.img = sub_right
                BIOMETYPE = BIOMETYPE=+1
                upgrades = False
                foundChest = False
                longerDiving = False
                diveBeneath = False
                player.gas = 100
                player.oxy = 100
                player.x = 0
                player.y = 0
                player.sonar_amount = 5
                whale.y = whale.y =- 300
                sonars = []
                if not musicPlaying:
                    musicPlaying = False
                else:
                    musicPlaying = True
            elif event.key == K_RETURN:
                if not paused and not upgrades:
                    if musicPlaying and player.sonar_amount > 0:
                        splash.play()
                    add_sonar()
            if event.key == ord('r') and not player.crushed:
                if not paused and not player.crushed and not upgrades:
                    if musicPlaying:
                        splash.play()
                player.diving = not player.diving
            if upgrades:
                if event.key == ord('1') and player.money >= 15 and player.gas != 100 and upgradePage == 1:
                    if musicPlaying:
                        cash.play()
                    player.gas = 100
                    player.money-=15
                elif event.key == ord('2') and player.money >= 40 and player.oxy != 100 and upgradePage == 1:
                    if musicPlaying:
                        cash.play()
                    player.oxy = 100
                    player.money-=40
                elif event.key == ord('3') and player.money >= 45 and upgradePage == 1:
                    if musicPlaying:
                        cash.play()
                    player.sonar_amount += 1
                    player.money-=45
                elif event.key == ord('d'):
                    if upgradePage == 2:
                        upgradePage = 1
                    else:
                        upgradePage = 2
                elif event.key == ord('a'):
                    if upgradePage == 2:
                        upgradePage = 1
                    else:
                        upgradePage = 2
                if upgradePage == 2:
                    if event.key == ord('1') and player.money >= 120 and lessRare == False:
                        if musicPlaying:
                            cash.play()
                        player.money -= 120
                        lessRare = True
                    if event.key == ord('2') and player.money >= 75 and longerDiving == False:
                        if musicPlaying:
                            cash.play()
                        player.money -= 75
                        longerDiving = True
                    if event.key == ord('3') and player.money >= 80 and diveBeneath == False:
                        if musicPlaying:
                            cash.play()
                        player.money -= 80
                        diveBeneath = True

            elif event.key == K_F11:
                FULLSCREENMODE = not FULLSCREENMODE
                if FULLSCREENMODE:
                    screen = pygame.display.set_mode((WIDTH,HEIGHT), FULLSCREEN) #Fullscreen
                else:
                    screen = pygame.display.set_mode((WIDTH,HEIGHT), 0, 32) #Normal screen
                
        if event.type == KEYUP:
            if event.key == ord('a') and player.movex<0:
                player.movex = 0
            elif event.key == ord('d') and player.movex>0:
                player.movex = 0
            elif event.key == ord('w') and player.movey<0:
                player.movey = 0
            elif event.key == ord('s') and player.movey>0:
                player.movey = 0

        #===END OF CHECKING EVENTS===

    if not player.crushed and not upgrades and not player.foundChest and paused == False:
        player.move()
        iceberg.move()
        check_iceberg_collision()
        if player.diving:
            chest=check_chests_collision()
            if chest:
                player.foundChest=True
                if chest.full:
                    player.money+=chest.gems
                    full=True
                else:
                    full=False
                    player.money+= chest.gems
                add_chest()
                chests.remove(chest)
                player.diving=False
            if longerDiving == False: #Checks if you have the longer diving upgrade
                DIVINGTIMER -= 1
            elif longerDiving == True:
                DIVINGTIMER -= 0.25
            player.oxy-=0.05
            if DIVINGTIMER == 0:
                player.diving = False
                DIVINGTIMER += (DIVINGTIMER+100)

        #===DRAWING===
    screen.blit(bg,(0,0))
    for sonar in sonars:
        screen.blit(sonar_display, (sonar.x-21, sonar.y-17))
        pygame.draw.circle(screen, sonar.color, ((sonar.x-1), (sonar.y+3)), 10)
        pygame.draw.circle(screen, BLACK, ((sonar.x-1), (sonar.y+3)), 10, 1)
        sonar.check_distance(chests)
    moveWhale()
    screen.blit(iceberg.img,(iceberg.x, iceberg.y))
    if player.diving == False:
        screen.blit(player.img,(player.x, player.y))
    if player.diving == True:
        pygame.draw.circle(screen, RED, ((player.x+32), (player.y+32)), 10, 1)        
    screen.blit(gem, (700, 5))
    screen.blit(sonar_display, (400, 0))
    if upgrades == True:
        if upgradePage == 1:
            screen.blit(upgrade_menu, (150, 40))
            ####################################################
            drawText('Gas - 15 gems', orbFont, screen, 320, 60, BLACK)
            drawText('Restores gas.', orbFont, screen, 320, 100, BLACK)
            drawText('Press 1.', orbFont, screen, 320, 140, BLACK)
            ####################################################
            drawText('Oxygen - 40 gems', orbFont, screen, 320, 200, BLACK)
            drawText('Restores oxygen.', orbFont, screen, 320, 240, BLACK)
            drawText('Press 2.', orbFont, screen, 320, 280, BLACK)
            ####################################################
            drawText('Sonar - 45 gems', orbFont, screen, 320, 340, BLACK)
            drawText('Buys a sonar.', orbFont, screen, 320, 380, BLACK)
            drawText('Press 3.', orbFont, screen, 320, 420, BLACK)
        else:
            screen.blit(upgrade_menu2, (150, 40))
            ####################################################
            drawText('Full chests are less rare.', orbFont, screen, 315, 60, BLACK)
            drawText('120 gems.', orbFont, screen, 315, 100, BLACK)
            drawText('Press 1.', orbFont, screen, 315, 140, BLACK)
            ####################################################
            drawText('You can dive for a longer time.', orbFont, screen, 310, 200, BLACK)
            drawText('75 gems.', orbFont, screen, 315, 240, BLACK)
            drawText('Press 2.', orbFont, screen, 315, 280, BLACK)
            ####################################################
            drawText('You can dive beneath the isle.', orbFont, screen, 315, 340, BLACK)
            drawText('80 gems.', orbFont, screen, 320, 380, BLACK)
            drawText('Press 3.', orbFont, screen, 320, 420, BLACK)
    if player.foundChest == True:
        screen.blit(img_chest, (280, 200))
        if full == False:
            screen.blit(empty_chest, (410, 245))
    drawText('x %s' % (player.money), orbFont, screen, 730, 10, WHITE)
    drawText('x %s' % (player.sonar_amount), orbFont, screen, 445, 5, WHITE)
    
    #draw_collision_rectangles - can be used as cheat...
    #for rect in player.current_rectangles+iceberg.current_rectangles: pygame.draw.rect(screen, WHITE, rect, 1)
    #for w in whale.current_rectangles: pygame.draw.rect(screen, WHITE, w, 1)
    #for chest in chests:
        #for rect in chest.current_rectangles:
            #pygame.draw.rect(screen, WHITE, rect, 1)
    #-------------------------
    clock.tick(80) #FPS
    if player.gas >= 50: #Start for different colors (gas/oxy display)
        drawText('Gas: %s, '% (int(player.gas)), orbFont, screen, 5, 3, WHITE)
    elif player.gas < 50 and player.gas >= 10:
        drawText('Gas: %s, '% (int(player.gas)), orbFont, screen, 5, 3, YELLOW)
    elif player.gas < 10:
        drawText('Gas: %s, '% (int(player.gas)), orbFont, screen, 5, 3, RED)
    if player.oxy >= 50:
        drawText('Oxygen: %s '% (int(player.oxy)), orbFont, screen, 115, 3, WHITE)
    elif player.oxy < 50 and player.oxy >= 10:
        drawText('Oxygen: %s '% (int(player.oxy)), orbFont, screen, 115, 3, YELLOW)
    elif player.oxy < 10:
        drawText('Oxygen: %s '% (int(player.oxy)), orbFont, screen, 115, 3, RED) #End
    if musicPlaying == False and not player.crushed:
        drawText('Muted', orbFont, screen, 5, 480, WHITE)
    if paused:
        drawText('Paused', orbFont, screen, 350, 210, WHITE)
    elif player.crushed:
        if player.gas <= 0:
            drawText('Out of gas! Game over.', orbFont, screen, 270, 210, WHITE)
            upgrades = False
        elif player.oxy <= 0:
            drawText('Out of oxygen! Game over.', orbFont, screen, 260, 210, WHITE)
            upgrades = False
        else:
            drawText('Your submarine has crushed! Game over.', orbFont, screen, 150, 200, WHITE)
        if musicPlaying == True:
            ice_crash.play()#Plays the crash sound
        musicPlaying = False
    pygame.display.update()
