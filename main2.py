import math
import random
import pygame
pygame.init()

sw = 800
sh = 800
newShipSound = pygame.mixer.Sound('extraShip.wav')
bangSound = pygame.mixer.Sound('bangSmall.wav')
bangLargeSound = pygame.mixer.Sound('bangLarge.wav')
thrustSound = pygame.mixer.Sound('thrust.wav')
fireSound = pygame.mixer.Sound('fire.wav')
beat1 = pygame.mixer.Sound('beat1.wav')
beat2 = pygame.mixer.Sound('beat2.wav')
music = pygame.mixer.music.load('dbzSong.mp3')
pygame.mixer.music.play(-1)

bg = pygame.image.load('starbg.png')
starImg = pygame.image.load('star.png')
life = pygame.image.load('rocketSil.png')
alienImg = pygame.image.load('alienShip.png')
rocketImg = pygame.image.load('rocketsmall.png')
ast150 =  pygame.image.load('asteroid150.png')
ast100 =  pygame.image.load('asteroid100.png')
ast50 =  pygame.image.load('asteroid50.png')
win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Game")
score = 0
highScore = 0
lives = 3
gameOver = False

clock = pygame.time.Clock()


class Alien(object):
    def __init__(self):
        self.img = alienImg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x = self.ranPoint[0]
        self.y = self.ranPoint[1]
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh/2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Player(object):
    def __init__(self):
        self.img = rocketImg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2# - self.w//2
        self.y = sh//2 #- self.h//2
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
        pygame.draw.rect(win, (255, 0, 0), [self.x, self.y, 3, 3])

    def turnLeft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x , self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x , self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def checkCollision(self, sprite1, sprite2):
        col = pygame.sprite.collide_rect(sprite1, sprite2)
        if col == True:
            global lives
            lives -= 1

class Star(object):
    def __init__(self):
        self.img = starImg
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x = self.ranPoint[0]
        self.y = self.ranPoint[1]
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh/2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

class PlayerBullet(object):
    def __init__(self):
        self.point = player.head
        self.x = self.point[0]
        self.y = self.point[1]
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.c * 12
        self.y -= self.s * 12

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

class AlienBullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 4
        self.dx, self.dy = player.x - self.x, player.y  - self.y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.dist, self.dy / self.dist  # Normalize.

        '''self.xdif = player.x - self.x
        self.ydif = player.y - self.y
        self.vtx = pygame.math.Vector2(player.x + player.w//2, self.x)
        self.vty = pygame.math.Vector2(player.y + player.h // 2, self.y)
        self.dirX = pygame.math.Vector2.normalize(self.vtx)
        self.dirY = pygame.math.Vector2.normalize(self.vty)'''
        self.xv = self.dx * 5
        self.yv = self.dy * 5


    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank#random.choice([1,1,1,1,2,2,3])
        if self.rank == 1:
            self.image = ast50
        elif self.rank == 2:
            self.image = ast100
        else:
            self.image = ast150
        self.w = 50 * self.rank
        self.h = 50 * self.rank
        self.ranPoint = random.choice([(random.randrange(0,sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh -self.h))])
        #self.f = (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh -self.h))
        self.x = self.ranPoint[0]
        self.y = self.ranPoint[1]
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh/2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


def redrawGameWindow():
    win.blit(bg, (0, 0))
    player.draw(win)
    for b in playerBullets:
        b.draw(win)
    for a in alienBullets:
        a.draw(win)
    for a in asteroids:
        a.draw(win)
    for i in range(lives):
        win.blit(life, (10 + i * 60, 10))
    for a in aliens:
        a.draw(win)
    for s in stars:
        s.draw(win)

    #Rapid Fire time Gauge
    if rapidFire:
        pygame.draw.rect(win, (0, 0, 0), [349, 19, 102, 22])
        pygame.draw.rect(win, (255, 255, 255), [350, 20, 100 - 100 * (count - rfStart)/500, 20])

    font = pygame.font.SysFont('arial', 30)
    scoreText = font.render('Score : ' + str(score), 1, (255, 255, 255))
    win.blit(scoreText, (sw - (scoreText.get_width()) - 20, 10))
    hiScoreText = font.render('High Score : ' + str(highScore), 1, (255, 255, 255))
    if highScore != 0:
        win.blit(hiScoreText, (sw - (hiScoreText.get_width()) - 20, 40))
    if gameOver:
        goText = font.render('Game Over :( ', 1, (255, 255, 255))
        paText = font.render('Press Space to Play Again ', 1, (255, 255, 255))
        win.blit(goText, (sw//2 - (goText.get_width())//2, sh//2 - goText.get_height()//2 -30))
        win.blit(paText, (sw // 2 - (paText.get_width()) // 2, sh // 2 - paText.get_height() // 2 + 30))

    # pong.draw(win)
    pygame.display.update()


player = Player()
playerBullets = []
alienBullets = []
asteroids = []
aliens = []
stars = []
rapidFire = False
rfStart = -1
count = 0
# space_ship_image = pygame.image.load(player).convert_alpha()
run = True
while run:
    clock.tick(60)
    count += 1
    if not gameOver:
        # New asteroid
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(ran))
        # new alien
        if count % 1000 == 0:
            aliens.append(Alien())

        # new life after 10,000 points
        '''if score % 1000 == 0 and score != 0:
            if lives + 1 <= 3:
                lives += 1
                newShipSound.play()'''

        # new Star
        if count % 1300 == 0:
            stars.append(Star())

        if player.angle == 360 or player.angle == -360:
            player.angle = 0
        for alien in aliens:
            alien.x += alien.xv
            alien.y += alien.yv
        if player.y + player.h < -5:
            player.y = sh - 10
        if player.y > sh + 5:
            player.y = -20
        if player.x + player.w < -5:
            player.x = sw - 10
        if player.x > sw:
            player.x = 0

        #Losing life check
        #for a in asteroids:
         #   coll = player.checkCollision(player.rotatedRect, a.image.get_rect())
          #  if coll:
           #     asteroids.pop(asteroids.index(a))

        for a in asteroids:
            '''player_rect = player.rotatedRect#pygame.Rect(player.x, player.y, player.w, player.h)
            a_rect = pygame.Rect(a.x, a.y, a.w, a.h)
            if player_rect.colliderect(a_rect):
                lives -= 1
                asteroids.pop(asteroids.index(a))'''
            if (player.x + 10 >= a.x and player.x - 10<= a.x + a.w):
                if (player. y + 10 >= a.y and player.y - 10<= a.y + a.h):

            #if (a.x >= player.x and a.x <= player.x + player.w) or (a.x + a.w>= player.x and a.x + a.w<= player.x + player.w):
             #   if (a.y >= player.y and a.y <= player.y + player.h) or (a.y + a.h >= player.y and a.y + a.h <= player.y + player.h):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    bangLargeSound.play()

        # Delete extra bullets
        for b in playerBullets:
            if b.x < -100 or b.x > sw + 100 or b.y < -100 or b.y > sh + 100:
                playerBullets.pop(playerBullets.index(b))
            # checking collisions
            for a in asteroids:
                if (b.x >= a.x and b.x <= a.x + a.w) or (b.x + b.w >= a.x and b.x + b.w <= a.x + a.w):
                    if (b.y >= a.y and b.y <= a.y + a.h) or (b.y + b.h >= a.y and b.y + b.h <= a.y + a.h):
                        if b in playerBullets:
                            playerBullets.pop(playerBullets.index(b))
                        if a.rank > 1:
                            if a.rank == 2:
                                score += 20
                            else:
                                score += 10
                            na1 = Asteroid(a.rank-1)
                            na1.x = a.x
                            na1.y = a.y
                            na2 = Asteroid(a.rank - 1)
                            na2.x = a.x
                            na2.y = a.y
                            na2.xv = na1.xv * -1
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                        bangSound.play()
                        asteroids.pop(asteroids.index(a))

        # asteroid motion and cleanup
        for a in asteroids:
            a.x += a.xv
            a.y += a.yv
            if a.x < - 200 or a.x > sw + 200 or a.y + a.h < -200 or a.y > sh + 200:
                asteroids.pop(asteroids.index(a))

        #alien shooting
        for a in aliens:
            if count % 30 == 0:
                alienBullets.append(AlienBullet(a.x + a.w//2, a.y + a.h//2))

        # Alien bullet motion:
        for b in alienBullets:
            b.x += b.xv
            b.y += b.yv

        # Killing alien
        for a in aliens:
            if a.x + a.w < -100 or a.x > sw + 100 or a.y > sh + 100 or a.y + a.h < -100:
                aliens.pop(aliens.index(a))
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or (b.x + b.w >= a.x and b.x + b.w <= a.x + a.w):
                    if (b.y >= a.y and b.y <= a.y + a.h) or (b.y + b.h >= a.y and b.y + b.h <= a.y + a.h):
                        if a in aliens:
                            score += 100
                            bangSound.play()
                            aliens.pop(aliens.index(a))

        # alien bullet hit player
        for a in alienBullets:
            if (a.x >= player.x - 10 and a.x <= player.x + 10) or (a.x + a.w >= player.x -10 and a.x + a.w <= player.x + 10):
                if (a.y >= player.y - 10 and a.y <= player.y + 10) or (a.y + a.h>= player.y - 10 and a.y + a.h<= player.y + 10):
                    alienBullets.pop(alienBullets.index(a))
                    bangLargeSound.play()
                    lives -= 1

        # player bullet and star collide
        for b in playerBullets:
            for s in stars:
                if b.x >= s.x and b.x <= s.x + s.w:
                    if b.y >= s.y and b.y <= s.y + s.h:
                        rapidFire = True
                        print("Rapid!")
                        stars.pop(stars.index(s))
                        rfStart = count
        # move stars
        for s in stars:
            s.x += s.xv
            s.y += s.yv

        # print(count - rfStart)
        # increment Rapid Fire Time:
        if rfStart != -1:
            if count - rfStart > 500:
                print('OVER')
                rapidFire = False
                rfStart = -1


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
            # thrustSound.play()


        # Use for TONS OF BULLETS
        if keys[pygame.K_SPACE] and rapidFire:
            playerBullets.append(PlayerBullet())
        if keys[pygame.K_a] and rapidFire:
            playerBullets.append(PlayerBullet())
        if keys[pygame.K_s]:
            rapidFire = True
        if keys[pygame.K_d]:
            rapidFire = False
        # playerBullets.append(PlayerBullet())
        #if keys[pygame.K_SPACE]:
            #playerBullets.append(PlayerBullet())

        #if len(playerBullets) > 0:
        for b in playerBullets:
            #b.x += b.c * 10
            #b.y -= b.s * 10
            b.move()

        if lives <= 0:
            gameOver = True
            if score > highScore:
                highScore = score


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Use for 1 bullet at a time
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameOver:
                    playerBullets.append(PlayerBullet())
                    fireSound.play()
                else:
                    gameOver = False
                    lives = 3
                    score = 0
                    count = 0
                    rfStart = -1
                    rapidFire = False

    redrawGameWindow()
pygame.quit()
