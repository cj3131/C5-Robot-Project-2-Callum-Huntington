import pygame
import time
import random
import sys
import csv
from pygame import * 
displayWidth = 800
displayHeight = 600
halfWidth = 400
halfHeight = 300
quadOne = (0,0)
quadTwo = (-800,0)
quadThree = (0,-352)
quadFour = (-800,-352)

#colour definition
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
brightRed = (255,0,0)
brightBlue = (0,0,255)
brightGreen = (0,255,0)

#Initialise screen
pygame.init()
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Bargain Hunter!")
clock = pygame.time.Clock()
fps = 60

spriteGroup = pygame.sprite.Group()
coinGroup = pygame.sprite.Group()
currentSpriteGroup = pygame.sprite.Group()
itemGroup = pygame.sprite.Group()

#Load player character, NPC, map, menu, and other interface images
eastImg = pygame.image.load('images/eastfacing.png')
eastLeftImg = pygame.image.load('images/eastfacingleft.png')
eastRightImg = pygame.image.load('images/eastfacingright.png')

westImg = pygame.image.load('images/westfacing.png')
westLeftImg = pygame.image.load('images/westfacingleft.png')
westRightImg = pygame.image.load('images/westfacingright.png')

northImg = pygame.image.load('images/northfacing.png')
northLeftImg = pygame.image.load('images/northfacingleft.png')
northRightImg = pygame.image.load('images/northfacingright.png')

southImg = pygame.image.load('images/southfacing.png')
southLeftImg = pygame.image.load('images/southfacingleft.png')
southRightImg = pygame.image.load('images/southfacingright.png')


shopkeepEastImg = pygame.image.load('images/shopkeepeastfacing.png') 
shopkeepEastLeftImg = pygame.image.load('images/shopkeepeastfacingleft.png') 
shopkeepEastRightImg = pygame.image.load('images/shopkeepeastfacingright.png') 

shopkeepWestImg = pygame.image.load('images/shopkeepwestfacing.png')
shopkeepWestLeftImg = pygame.image.load('images/shopkeepwestfacingleft.png') 
shopkeepWestRightImg = pygame.image.load('images/shopkeepwestfacingright.png') 

shopkeepNorthImg = pygame.image.load('images/shopkeepnorthfacing.png') 
shopkeepNorthLeftImg = pygame.image.load('images/shopkeepnorthfacingleft.png') 
shopkeepNorthRightImg = pygame.image.load('images/shopkeepnorthfacingright.png') 

shopkeepSouthImg = pygame.image.load('images/shopkeepsouthfacing.png') 
shopkeepSouthLeftImg = pygame.image.load('images/shopkeepsouthfacingleft.png') 
shopkeepSouthRightImg = pygame.image.load('images/shopkeepsouthfacingright.png') 


mapImg = pygame.image.load("images/mainmap.png")
shopImg = pygame.image.load('images/shopinteriorone.png')
startImg = pygame.image.load('images/startmenu.png')
scrollImg = pygame.image.load('images/scrollhorizontal.png')
coinImg = pygame.image.load('images/coinone.png')

#Used to move the NPC character in shops around.
class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.xChange = 0
        self.yChange = 0

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def setImage(self,filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

#Items found in shops.
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()

    def setImage(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

#A sprite to be used in detecting when the player character picks up a coin.
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()

    def setImage(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y
        

#Deals with the player character's movement, and changing of map quadrants
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        #self.sound = pygame.mixer.Sound("walking.wav")
        self.sector = "topleft"
        self.collided = False
        self.coins = 0
        self.collected = []

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def setImage(self, filename):
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()

    def playSound(self):
        self.sound.play()

    def move(self, direction):
        t = 0
        if direction == None:
            return
        elif direction == "west":
            imgOne = westImg
            imgTwo = westLeftImg
            imgThree = westRightImg
            xChange = -1
            yChange = 0
        elif direction == "east":
            imgOne = eastImg
            imgTwo = eastLeftImg
            imgThree = eastRightImg
            xChange = 1
            yChange = 0
        elif direction == "south":
            imgOne = southImg
            imgTwo = southLeftImg
            imgThree = southRightImg
            xChange = 0
            yChange = 1
        else:
            imgOne = northImg
            imgTwo = northLeftImg
            imgThree = northRightImg
            xChange = 0
            yChange = -1
            

        if self.sector == "topleft":
            if (c1 not in self.collected):
                currentSpriteGroup.add(c1)
            if (c2 not in self.collected):
                currentSpriteGroup.add(c2)
            if (c3 not in self.collected):
                currentSpriteGroup.add(c3)
            if (self.rect.x + xChange) < 65 or (self.rect.y + yChange) < 65:
                print("collided")
                self.collided = True
            elif (self.rect.x + xChange) > 769:
                self.sector = "topright"
                self.rect.x = -31
                self.collided = False
                currentSpriteGroup.empty()
                if (c4 not in self.collected):
                    currentSpriteGroup.add(c4)
                currentSpriteGroup.add(pc, checkout)
            elif (self.rect.y + yChange) > 577:
                self.sector = "bottomleft"
                self.rect.y = 225
                self.collided = False
                currentSpriteGroup.empty()
                if (c7 not in self.collected):
                    currentSpriteGroup.add(c7)
                if (c8 not in self.collected):
                    currentSpriteGroup.add(c8)
                if (c9 not in self.collected):
                    currentSpriteGroup.add(c9)
                currentSpriteGroup.add(pc)
            else:
                self.collided = False

        elif self.sector == "topright":
            if (c4 not in self.collected):
                currentSpriteGroup.add(c4)
            if (self.rect.x == 353 or self.rect.x == 385) and (self.rect.y == 65):
                pass
            elif (self.rect.x == 353 and self.rect.y == 33 and xChange == 1) or (self.rect.x == 385 and self.rect.y == 33 and xChange == -1):
                self.collided = False
            elif (self.rect.x == 353 or self.rect.x == 385) and (self.rect.y == 33):
                if xChange == 1 or xChange == -1 or yChange == -1 :
                    print("collided")
                    self.collided = True
                else:
                    self.collided = False
            elif (self.rect.x + xChange) > 705 or (self.rect.y + yChange) < 65:
                print("collided")
                self.collided = True
            elif ( (self.rect.x == 609) and (193 < self.rect.y + yChange < 225) ) or ( (self.rect.x == 641) and (193 < self.rect.y + yChange < 225) ):
                shopInterior(imgOne,shopImg,"phones")
                self.rect.x, self.rect.y = 641,225
                yChange = 1
                direction = None
                itemGroup.empty()
                itemGroup.add(i1,i2,i3,i4,i5,i6)
            elif (self.rect.x + xChange) < 1:
                self.sector = "topleft"
                self.rect.x = 801
                self.collided = False
                currentSpriteGroup.empty()
                if (c1 not in self.collected):
                    currentSpriteGroup.add(c1)
                if (c2 not in self.collected):
                    currentSpriteGroup.add(c2)
                if (c3 not in self.collected):
                    currentSpriteGroup.add(c3)
                currentSpriteGroup.add(pc)
            elif (self.rect.y + yChange) > 577:
                self.sector = "bottomright"
                self.rect.y = 225
                self.collided = False
                currentSpriteGroup.empty()
                if (c5 not in self.collected):
                    currentSpriteGroup.add(c5)
                if (c6 not in self.collected):
                    currentSpriteGroup.add(c6)
                currentSpriteGroup.add(pc)
            else:
                self.collided = False

        elif self.sector == "bottomleft":
            if (c7 not in self.collected):
                currentSpriteGroup.add(c7)
            if (c8 not in self.collected):
                currentSpriteGroup.add(c8)
            if (c9 not in self.collected):
                currentSpriteGroup.add(c9)
            if (self.rect.x + xChange) < 65 or (self.rect.y + yChange) > 481:
                print("collided")
                self.collided = True
            elif ( (self.rect.x == 161) and (417 < self.rect.y + yChange < 449) ) or ( (self.rect.x == 193) and (417 < self.rect.y + yChange < 449) ):
                shopInterior(imgOne,shopImg,"consoles")
                self.rect.x, self.rect.y = 161, 449
                yChange = 1
                direction = None
                itemGroup.empty()
                itemGroup.add(i1,i2,i3,i4,i5,i6)
            elif (self.rect.x + xChange) > 769:
                self.sector = "bottomright"
                self.rect.x = -31
                self.collided = False
                currentSpriteGroup.empty()
                if (c5 not in self.collected):
                    currentSpriteGroup.add(c5)
                if (c6 not in self.collected):
                    currentSpriteGroup.add(c6)
                currentSpriteGroup.add(pc)
            elif (self.rect.y + yChange) < 1:
                self.sector = "topleft"
                self.rect.y = 353
                self.collided = False
                currentSpriteGroup.empty()
                if (c1 not in self.collected):
                    currentSpriteGroup.add(c1)
                if (c2 not in self.collected):
                    currentSpriteGroup.add(c2)
                if (c3 not in self.collected):
                    currentSpriteGroup.add(c3)
                currentSpriteGroup.add(pc)
            else:
                self.collided = False

        elif self.sector == "bottomright":
            if (c5 not in self.collected):
                currentSpriteGroup.add(c5)
            if (c6 not in self.collected):
                currentSpriteGroup.add(c6)
            if (self.rect.x + xChange) > 705 or (self.rect.y + yChange) > 481:
                print("collided")
                self.collided = True
            elif ((self.rect.x == 545) and (417 < self.rect.y + yChange < 449)) or ((self.rect.x == 577) and (417 < self.rect.y + yChange < 449)):
                shopInterior(imgOne,shopImg,"laptop")
                self.rect.x, self.rect.y = 577,449
                yChange = 1
                direction = None
                itemGroup.empty()
                itemGroup.add(i1,i2,i3,i4,i5,i6)
            elif (self.rect.x + xChange) < 1:
                self.sector = "bottomleft"
                self.rect.x = 801
                self.collided = False
                currentSpriteGroup.empty()
                if (c7 not in self.collected):
                    currentSpriteGroup.add(c7)
                if (c8 not in self.collected):
                    currentSpriteGroup.add(c8)
                if (c9 not in self.collected):
                    currentSpriteGroup.add(c9)
                currentSpriteGroup.add(pc)
            elif (self.rect.y + yChange) < 1:
                self.sector = "topright"
                self.rect.y = 353
                self.collided = False
                currentSpriteGroup.empty()
                if (c4 not in self.collected):
                    currentSpriteGroup.add(c4)
                currentSpriteGroup.add(pc, checkout)
            else:
                self.collided = False


        if self.collided == True:
            self.image = imgOne
            update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
        else:
            while t < 31:
                for i in range(4):
                    self.image = imgTwo
                    self.rect.x, self.rect.y = update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                    pygame.time.delay(5)
                    t += 1

                for i in range(4):
                    self.image = imgOne
                    self.rect.x, self.rect.y = update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                    pygame.time.delay(5)
                    t += 1

                for i in range(4):
                    self.image = imgThree
                    self.rect.x, self.rect.y = update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                    pygame.time.delay(5)
                    t += 1

                for i in range (4):
                    self.image = imgOne
                    self.rect.x, self.rect.y = update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                    pygame.time.delay(5)
                    t += 1

            if self.sector == "topleft":
                if pygame.sprite.collide_rect(pc,c1) and (c1 not in self.collected):
                    print("You got c1")
                    self.coins += 1
                    self.collected.append(c1)
                    c1.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                elif pygame.sprite.collide_rect(pc,c2) and (c2 not in self.collected):
                    print("You got c2")
                    self.coins += 1
                    self.collected.append(c2)
                    c2.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                elif pygame.sprite.collide_rect(pc,c3) and (c3 not in self.collected):
                    print("You got c3")
                    self.coins += 1
                    self.collected.append(c3)
                    c3.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)

            elif self.sector == "topright":
                if pygame.sprite.collide_rect(pc,c4) and (c4 not in self.collected):
                    print("You got c4")
                    self.coins += 1
                    self.collected.append(c4)
                    c4.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)

            elif self.sector == "bottomleft":
                if pygame.sprite.collide_rect(pc,c7) and (c7 not in self.collected):
                    print("You got c7")
                    self.coins += 1
                    self.collected.append(c7)
                    c7.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                elif pygame.sprite.collide_rect(pc,c8) and (c8 not in self.collected):
                    print("You got c8")
                    self.coins += 1
                    self.collected.append(c8)
                    c8.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                elif pygame.sprite.collide_rect(pc,c9) and (c9 not in self.collected):
                    print("You got c9")
                    self.coins += 1
                    self.collected.append(c9)
                    c9.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)

            elif self.sector == "bottomright":
                if pygame.sprite.collide_rect(pc,c5) and (c5 not in self.collected):
                    print("You got c5")
                    self.coins += 1
                    self.collected.append(c5)
                    c5.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)
                elif pygame.sprite.collide_rect(pc,c6) and (c6 not in self.collected):
                    print("You got c6")
                    self.coins += 1
                    self.collected.append(c6)
                    c6.remove(currentSpriteGroup)
                    update(self.rect.x, self.rect.y, xChange, yChange, self.sector, mapImg, currentSpriteGroup)

            xChange = 0
            yChange = 0
            print(self.rect)
        return direction

#This function should be called every time something happens, i.e when the character moves.
def update(posx, posy, xChange, yChange, sect, img, currentSpriteGroup):
    posx += xChange
    posy += yChange
    gameDisplay.fill(white)

    if sect == "topleft":
        gameDisplay.blit(img, (0,0))        
    elif sect == "topright":
        gameDisplay.blit(img, (-800,0))
    elif sect == "bottomleft":
        gameDisplay.blit(img, (0,-352))
    elif sect == "bottomright":
        gameDisplay.blit(img, (-800,-352))

    currentSpriteGroup.draw(gameDisplay)
    pygame.display.update()
    return posx, posy

#This function should run when entering a shop. 
def shopInterior(player, shopBackground, itemtype):
    inside = True
    result = False
    pc.rect.x = 417
    pc.rect.y = 545
    gameDisplay.fill(white)
    gameDisplay.blit(shopBackground, (0,0))
    gameDisplay.blit(scrollImg, (80,0))
    shopkeeper = NPC()
    shopkeeper.setImage("images/shopkeepsouthfacing.png")
    shopkeeper.setPosition(416, 481)

    if itemtype == "laptop":
        for i in itemGroup:
            i.setImage ("images/computer.png")
    elif itemtype == "consoles":
        for i in itemGroup:
            i.setImage("images/console.png")
    elif itemtype == "phones":
        for i in itemGroup:
            i.setImage("images/phone.png")
    i1.setPosition(97, 97)
    i2.setPosition(417, 417)
    i3.setPosition(65, 97)
    i4.setPosition(97, 129)
    i5.setPosition(257, 129)
    i6.setPosition(193, 161)

    spriteGroup.add(shopkeeper)
    spriteGroup.draw(gameDisplay)
    writeText("Hello. How long do you", "freesansbold.ttf", 36, 160,80)
    writeText("want me to search for?", "freesansbold.ttf", 36, 160,120)
    writeText("1 minute", "freesansbold.ttf", 24, 160, 300)
    writeText("2 minutes", "freesansbold.ttf", 24, 290, 300)
    writeText("3 minutes", "freesansbold.ttf", 24, 425, 300)
    writeText("Exit", "freesansbold.ttf", 24, 565, 300)
    writeText("(costs 1 coin)", "freesansbold.ttf", 16, 160, 325)
    writeText("(costs 2 coins)", "freesansbold.ttf", 16, 290, 325)
    writeText("(costs 3 coins)", "freesansbold.ttf", 16, 425, 325)
    pygame.display.update()


    #Here we check the user's option choice
    while inside == True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit("Exiting")
                quit()

            result = button (160, 300, 110, 50, result)
            if result == True:
                if pc.coins >= 1:
                    print("You have enough coins. Searching for 1 minute")
                    gameDisplay.fill(white)
                    gameDisplay.blit(shopBackground, (0,0))
                    spriteGroup.draw(gameDisplay)
                    itemGroup.draw(gameDisplay)
                    pygame.display.update()
                    while i2.rect.x < shopkeeper.rect.x or  i2.rect.x > shopkeeper.rect.x:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i2.rect.x < shopkeeper.rect.x:
                            shopkeeper.rect.x -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i2.rect.x > shopkeeper.rect.x:
                            shopkeeper.rect.x += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                    while i2.rect.y > shopkeeper.rect.y or i2.rect.y < shopkeeper.rect.y:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i2.rect.y > shopkeeper.rect.y:
                            shopkeeper.rect.y += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i2.rect.y < shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    i2.remove(itemGroup)

                    while i5.rect.x < shopkeeper.rect.x or  i5.rect.x > shopkeeper.rect.x:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i5.rect.x < shopkeeper.rect.x:
                            shopkeeper.rect.x -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i5.rect.x > shopkeeper.rect.x:
                            shopkeeper.rect.x += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                    while i5.rect.y > shopkeeper.rect.y or i5.rect.y < shopkeeper.rect.y:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i5.rect.y > shopkeeper.rect.y:
                            shopkeeper.rect.y += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i5.rect.y < shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    i5.remove(itemGroup)
                        
                    if itemtype == "laptop":
                        f = open('laptoplist', 'r')
                    elif itemtype == "phones":
                        f = open('phonelist', 'r')
                    elif itemtype == "consoles":
                        f = open('consolelist', 'r')
                    j = 0
                    fcollected = open("collecteditems", "w")
                    for line in f:
                        fcollected.write(line)
                        j += 1
                        if j == 2:
                            break
                    fcollected.close()
                    f.close()
                    shopkeeper.remove(spriteGroup)
                    #fcollected = open('collecteditems', 'r')
                    #text = fcollected.read()
                    #print(text)
                    return
                else:
                    print("You do not have enough coins.")

            result = button(290, 300, 110, 30, result)
            if result == True:
                    if pc.coins >= 2:
                        print("You have enough coins. Searching for 2 minutes")
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        spriteGroup.draw(gameDisplay)
                        itemGroup.draw(gameDisplay)
                        pygame.display.update()
                        while i2.rect.x < shopkeeper.rect.x or  i2.rect.x > shopkeeper.rect.x:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i2.rect.x < shopkeeper.rect.x:
                                shopkeeper.rect.x -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i2.rect.x > shopkeeper.rect.x:
                                shopkeeper.rect.x += 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                        while i2.rect.y > shopkeeper.rect.y or i2.rect.y < shopkeeper.rect.y:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i2.rect.y > shopkeeper.rect.y:
                                shopkeeper.rect.y -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i2.rect.y < shopkeeper.rect.y:
                                shopkeeper.rect.y -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)

                        i2.remove(itemGroup)

                        while i5.rect.x < shopkeeper.rect.x or  i5.rect.x > shopkeeper.rect.x:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i5.rect.x < shopkeeper.rect.x:
                                shopkeeper.rect.x -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i5.rect.x > shopkeeper.rect.x:
                                shopkeeper.rect.x += 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                        while i5.rect.y > shopkeeper.rect.y or i5.rect.y < shopkeeper.rect.y:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i5.rect.y > shopkeeper.rect.y:
                                shopkeeper.rect.y -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i5.rect.y < shopkeeper.rect.y:
                                shopkeeper.rect.y -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)

                        i5.remove(itemGroup)

                        while i6.rect.x < shopkeeper.rect.x or  i6.rect.x > shopkeeper.rect.x:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i6.rect.x < shopkeeper.rect.x:
                                shopkeeper.rect.x -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i6.rect.x > shopkeeper.rect.x:
                                shopkeeper.rect.x += 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                        while i6.rect.y > shopkeeper.rect.y or i6.rect.y < shopkeeper.rect.y:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i6.rect.y > shopkeeper.rect.y:
                                shopkeeper.rect.y += 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i6.rect.y < shopkeeper.rect.y:
                                shopkeeper.rect.y += 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)

                        i6.remove(itemGroup)

                        while i4.rect.x < shopkeeper.rect.x or  i4.rect.x > shopkeeper.rect.x:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i4.rect.x < shopkeeper.rect.x:
                                shopkeeper.rect.x -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i4.rect.x > shopkeeper.rect.x:
                                shopkeeper.rect.x += 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                        while i4.rect.y > shopkeeper.rect.y or i4.rect.y < shopkeeper.rect.y:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i4.rect.y > shopkeeper.rect.y:
                                shopkeeper.rect.y -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i4.rect.y < shopkeeper.rect.y:
                                shopkeeper.rect.y -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)

                        i4.remove(itemGroup)
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground,(0,0))
                        spriteGroup.draw(gameDisplay)
                        itemGroup.draw(gameDisplay)
                        pygame.display.update()

                        if itemtype == "laptop":
                            f = open('laptoplist', 'r')
                        elif itemtype == "phones":
                            f = open('phonelist', 'r')
                        elif itemtype == "consoles":
                            f = open('consolelist', 'r')

                        j = 0
                        fcollected = open("collecteditems", "w")
                        for line in f:
                            fcollected.write(line)
                            j += 1
                            if j == 4:
                                break
                        fcollected.close()
                        f.close()
                        shopkeeper.remove(spriteGroup)
                        return

                    else:
                        print("You do not have enough coins.")

            result = button(425, 300, 110, 30, result)
            if result == True:
                if pc.coins >= 3:
                    print("You have enough coins. Searching for 3 minutes")
                    gameDisplay.fill(white)
                    gameDisplay.blit(shopBackground, (0,0))
                    spriteGroup.draw(gameDisplay)
                    itemGroup.draw(gameDisplay)
                    pygame.display.update()
                    while i2.rect.x < shopkeeper.rect.x or  i2.rect.x > shopkeeper.rect.x:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i2.rect.x < shopkeeper.rect.x:
                            shopkeeper.rect.x -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i2.rect.x > shopkeeper.rect.x:
                            shopkeeper.rect.x += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    while i2.rect.y > shopkeeper.rect.y or i2.rect.y < shopkeeper.rect.y:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i2.rect.y > shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i2.rect.y < shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    i2.remove(itemGroup)

                    while i5.rect.x < shopkeeper.rect.x or  i5.rect.x > shopkeeper.rect.x:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i5.rect.x < shopkeeper.rect.x:
                            shopkeeper.rect.x -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i5.rect.x > shopkeeper.rect.x:
                            shopkeeper.rect.x += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    while i5.rect.y > shopkeeper.rect.y or i5.rect.y < shopkeeper.rect.y:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i5.rect.y > shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i5.rect.y < shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    i5.remove(itemGroup)
                        
                    while i6.rect.x < shopkeeper.rect.x or  i6.rect.x > shopkeeper.rect.x:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i6.rect.x < shopkeeper.rect.x:
                            shopkeeper.rect.x -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i6.rect.x > shopkeeper.rect.x:
                            shopkeeper.rect.x += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    while i6.rect.y > shopkeeper.rect.y or i6.rect.y < shopkeeper.rect.y:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i6.rect.y > shopkeeper.rect.y:
                            shopkeeper.rect.y += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i6.rect.y < shopkeeper.rect.y:
                            shopkeeper.rect.y += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    i6.remove(itemGroup)

                    while i4.rect.x < shopkeeper.rect.x or  i4.rect.x > shopkeeper.rect.x:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i4.rect.x < shopkeeper.rect.x:
                            shopkeeper.rect.x -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i4.rect.x > shopkeeper.rect.x:
                            shopkeeper.rect.x += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    while i4.rect.y > shopkeeper.rect.y or i4.rect.y < shopkeeper.rect.y:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i4.rect.y > shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i4.rect.y < shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    i4.remove(itemGroup)
                                
                    while i1.rect.x < shopkeeper.rect.x or  i1.rect.x > shopkeeper.rect.x:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i1.rect.x < shopkeeper.rect.x:
                            shopkeeper.rect.x -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i1.rect.x > shopkeeper.rect.x:
                            shopkeeper.rect.x += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    while i1.rect.y > shopkeeper.rect.y or i1.rect.y < shopkeeper.rect.y:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i1.rect.y > shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i1.rect.y < shopkeeper.rect.y:
                            shopkeeper.rect.y -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                    i1.remove(itemGroup)

                    while i3.rect.x < shopkeeper.rect.x or  i3.rect.x > shopkeeper.rect.x:
                        gameDisplay.fill(white)
                        gameDisplay.blit(shopBackground, (0,0))
                        if i3.rect.x < shopkeeper.rect.x:
                            shopkeeper.rect.x -= 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)
                        elif i3.rect.x > shopkeeper.rect.x:
                            shopkeeper.rect.x += 1
                            spriteGroup.draw(gameDisplay)
                            itemGroup.draw(gameDisplay)
                            pygame.display.update()
                            pygame.time.delay(30)

                        while i3.rect.y > shopkeeper.rect.y or i3.rect.y < shopkeeper.rect.y:
                            gameDisplay.fill(white)
                            gameDisplay.blit(shopBackground, (0,0))
                            if i3.rect.y > shopkeeper.rect.y:
                                shopkeeper.rect.y -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)
                            elif i3.rect.y < shopkeeper.rect.y:
                                shopkeeper.rect.y -= 1
                                spriteGroup.draw(gameDisplay)
                                itemGroup.draw(gameDisplay)
                                pygame.display.update()
                                pygame.time.delay(30)

                    i3.remove(itemGroup)

                    if itemtype == "laptop":
                        f = open('laptoplist', 'r')
                    elif itemtype == "phones":
                        f = open('phonelist', 'r')
                    elif itemtype == "consoles":
                        f = open('consolelist', 'r')
                        
                    j = 0
                    fcollected = open("collecteditems", "w")
                    for line in f:
                        fcollected.write(line)
                        j += 1
                        if j == 6:
                            break
                    fcollected.close()
                    f.close()
                    shopkeeper.remove(spriteGroup)
                    return
                            
                else:
                    print("You do not have enough coins.")

            result = button(565, 300, 110, 25, result)
            if result == True:
                print("Exit")
                shopkeeper.remove(spriteGroup)
                return

# end game sorting. 
def collected_items():
    result = None
    showingCollected = True
    #mapImg = pygame.image.load("images/mainmap.png")
    #scrollImg = pygame.image.load("images/scrollhorizontal.png")
    gameDisplay.fill(white)
    gameDisplay.blit(mapImg,(-800,0))
    currentSpriteGroup.draw(gameDisplay)
    gameDisplay.blit(scrollImg,(80,0))
    writeText("Here are your items so far", "freesansbold.ttf", 36, 160, 80)
    writeText("Price", "freesansbold.ttf", 36, 160, 500)
    writeText("Exit", "freesansbold.ttf", 36, 600, 500)
    pygame.display.update()
    print("Got to here")

    while showingCollected == True:
        sortedAttributeList=[]
        collectedDict = {}
        sortedCollectedList = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showingCollected = False
                pygame.quit()
                sys.exit("Exiting")
                quit()

            writeText("Price", "freesansbold.ttf", 36, 160, 500)
            result = button (160, 500, 110, 50, result)
            if result == True:
                with open('laptoplist', 'r') as f:
                    reader = csv.reader(f)
                    for line in reader:
                        print("line is",line)
                        print("line 2 is",line[2])
                        collectedDict[line[2]] = line
                        print("collectedDict is",collectedDict)
                        sortedAttributeList.append(line[2])
                        print("sortedAttributeList is", sortedAttributeList)
                bubblesort(sortedAttributeList)
                print("now sortedAttributeList is", sortedAttributeList)
                newDictKey = 0
                for i in sortedAttributeList:
                    sortedCollectedList.append(collectedDict[i])
                    print("This sortedAttributeList is", sortedCollectedList)
                gameDisplay.fill(white)
                gameDisplay.blit(mapImg, (-800, 0))
                currentSpriteGroup.draw(gameDisplay)
                gameDisplay.blit(scrollImg, (80, 0))
                textposy = 100
                for i in range(len(sortedCollectedList)):
                    writeText(str(sortedCollectedList[i]), "freesansbold.ttf", 32, 160, textposy)
                    textposy += 30

            writeText("Rating", "freesansbold.ttf", 36, 300, 500)
            result = button(300, 500, 110, 50, result)
            if result == True:
                with open('laptoplist', 'r') as f:
                    reader = csv.reader(f)
                    for line in reader:
                        print("line is",line)
                        print("line 3 is",line[3])
                        collectedDict[line[3]] = line
                        print("collectedDict is",collectedDict)
                        sortedAttributeList.append(line[3])
                        print("sortedAttributeList is", sortedAttributeList)
                bubblesort(sortedAttributeList)
                print("now sortedAttributeList is", sortedAttributeList)
                newDictKey = 0
                for i in sortedAttributeList:
                    sortedCollectedList.append(collectedDict[i])
                    print("This sortedAttributeList is", sortedCollectedList)
                gameDisplay.fill(white)
                gameDisplay.blit(mapImg, (-800, 0))
                currentSpriteGroup.draw(gameDisplay)
                gameDisplay.blit(scrollImg, (80, 0))
                textposy = 100
                for i in range(len(sortedCollectedList)):
                    writeText(str(sortedCollectedList[i]), "freesansbold.ttf", 32, 160, textposy)
                    textposy += 30

            result = button(600,500,110,50,result)
            writeText("Exit", "freesansbold.ttf", 36, 600, 500)
            pygame.display.update()
            if result == True:
                update(pc.rect.x, pc.rect.y, 0, 0, "topright", mapImg, currentSpriteGroup)
                return

#bubblesort function
def bubblesort (alist):
    for passnum in range(len(alist)-1,0,-1):
                          for i in range (passnum):
                            if alist[i]>alist[i+1]:
                                temp = alist[i]
                                alist[i] = alist[i+1]
                                alist[i+1] = temp
    return(alist)
                
def coincollecting(posx, posy, item):
    while item.rect.x < shopkeeper.rect.x or  item.rect.x > shopkeeper.rect.x:
        if item.rect.x < shopkeeper.rect.x:
            shopkeeper.rect.x -= 1
            spriteGroup.draw(gameDisplay)
            itemGroup.draw(gameDisplay)
            pygame.display.update()
            pygame.time.delay(500)
        elif item.rect.x > shopkeeper.rect.x:
            shopkeeper.rect.x += 1
            spriteGroup.draw(gameDisplay)
            itemGroup.draw(gameDisplay)
            pygame.display.update()
            pygame.time.delay(500)
        while item.rect.y > shopkeeper.rect.y or item.rect.y < shopkeeper.rect.y:
            gameDisplay.fill(white)
            gameDisplay.blit(shopBackground, (0,0))
            if item.rect.y > shopkeeper.rect.y:
                shopkeeper.rect.y -= 1
                spriteGroup.draw(gameDisplay)
                itemGroup.draw(gameDisplay)
                pygame.display.update()
                pygame.time.delay(500)
            elif item.rect.y < shopkeeper.rect.y:
                shopkeeper.rect.y -= 1
                spriteGroup.draw(gameDisplay)
                itemGroup.draw(gameDisplay)
                pygame.display.update()
                pygame.time.delay(500)
                
#If the user clicks within the given co-ords, the passed function will run
def button(x,y,w,h,chosen):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    chosen = False
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1:
            chosen = True
    return chosen

#Writes text in specified location
def writeText(text,fontType,fontSize,x,y):
    font = pygame.font.Font(fontType, fontSize)
    text = font.render(text, 1, (10,10,10))
    textRect = text.get_rect()
    textRect = (x,y)
    gameDisplay.blit(text, textRect)

#Main menu function
def gameIntro():
    result = False
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit("Exiting")
                quit()
            gameDisplay.fill(white)    
            gameDisplay.blit (startImg, (0,0))
            result = button (5,526,105,48,result)
            if result == True:
                return
            result = button (438,526,105,48,result)
            if result == True:
                pygame.quit()
                sys.exit("Exiting")
                quit()
            pygame.display.update()
            clock.tick(15)


def gameLoop():
    
    pc.setImage("images/southfacing.png")
    for i in coinGroup:
        i.setImage("images/coinone.png")
    for i in itemGroup:
        i.setImage ("images/coinone.png")
    checkout.setImage("images/checkout.png")

    pc.setPosition(193, 97)
    checkout.setPosition(129, 257)
    c1.setPosition(545, 289)
    c2.setPosition(673, 97)
    c3.setPosition(385, 97)
    c4.setPosition(353, 33)
    c5.setPosition(225, 417)
    c6.setPosition(1, 257)
    c7.setPosition(737, 449)
    c8.setPosition(481, 449)
    c9.setPosition(513, 257)
    

    gameDisplay.fill(white)
    gameDisplay.blit(mapImg, (0, 0))
    currentSpriteGroup.draw(gameDisplay)
    pygame.display.update()
    direction = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit("Exiting")
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "west"
                if event.key == pygame.K_RIGHT:
                    direction = "east"
                if event.key == pygame.K_UP:
                    direction = "north"
                if event.key == pygame.K_DOWN:
                    direction = "south"
                if event.key == pygame.K_SPACE:
                    if pc.rect.x == 129 and pc.rect.y == 289:
                        collected_items()
                        direction = None
                    else:
                        direction = None
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    direction = None
        direction = pc.move(direction)
        clock.tick(fps)

pc = Player()
c1,c2,c3,c4,c5,c6,c7,c8,c9 = Coin(),Coin(),Coin(),Coin(),Coin(),Coin(),Coin(),Coin(),Coin()
i1,i2,i3,i4,i5,i6 = Item(),Item(),Item(),Item(),Item(),Item()
checkout = NPC()

itemGroup.add(i1,i2,i3,i4,i5,i6)
coinGroup.add(c1,c2,c3,c4,c5,c6,c7,c8,c9)
spriteGroup.add(pc)
currentSpriteGroup.add(pc,c1,c2,c3)



gameIntro()
gameLoop()
pygame.quit()
sys.exit("Exiting")
quit()
