import math
import random
import pygame
pygame.init()

sw = 800
sh = 800
bg = pygame.image.load('bg2.png')
rocketImg = pygame.image.load('rocketsmall.png')

win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Game")

clock = pygame.time.Clock()


class Player(object):
    def __init__(self):
        self.img = rocketImg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2 - self.w//2
        self.y = sh//2 - self.h//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x , self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)


    def draw(self, win):
        win.blit(self.rotatedSurf, self.rotatedRect)
        #win.blit(self.img, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), [self.head[0], self.head[1], 3, 3])

    def turnLeft(self):
        self.angle += 10
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x , self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def turnRight(self):
        self.angle -= 10
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x , self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def moveForward(self):
        self.x += self.cosine * 10
        self.y -= self.sine * 10
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

class PlayerBullet(object):
    def __init__(self):
        self.point = player.head
        self.x = self.point[0]
        self.y = self.point[1]
        self.w = 10
        self.h = 10
        self.c = player.cosine
        self.s = player.sine

    def move(self):
        self.x += self.c * 10
        self.y -= self.s * 10

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), [self.point[0], self.point[1], 3, 3])



def redrawGameWindow():
    #win.blit(bg, (0, 0))
    player.draw(win)
    for b in playerBullets:
        b.draw(win)
    font = pygame.font.SysFont('comicsans', 50)
    # scoreText = font.render(str(p1score), 1, (255, 255, 255))
    # win.blit(score1, (sw - (score1.get_width()) - 20, 30))
    # pong.draw(win)
    pygame.display.update()

player = Player()
playerBullets = []

# space_ship_image = pygame.image.load(player).convert_alpha()
run = True
while run:
    clock.tick(60)
    if player.angle == 360 or player.angle == -360:
        player.angle = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.turnLeft()
        #print(str(player.angle), str(math.cos(math.radians(player.angle + 90))))
    if keys[pygame.K_RIGHT]:
        player.turnRight()
        #print(str(player.angle), str(math.cos(player.angle)))
        #print(player.head)
    if keys[pygame.K_UP]:
        player.moveForward()
    if keys[pygame.K_SPACE]:
        playerBullets.append(PlayerBullet())

    if len(playerBullets) > 0:
        for b in playerBullets:
            #b.x += b.c * 10
            #b.y -= b.s * 10
            b.move()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    redrawGameWindow()
pygame.quit()
