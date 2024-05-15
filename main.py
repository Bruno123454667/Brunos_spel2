import math
import random
import pygame
from pygame import mixer
import time

# Intialize the pygame
pygame.init()

# skapar rutan
screen = pygame.display.set_mode((800, 600))  # Höjd och bredd

# Bakgrunden
background = pygame.image.load('bakgrund.png')  # Väljer bild

# Bakgrunds musik
mixer.music.load('bakgrunds musik1.mp3')  # Musik
mixer.music.play(-1)  # Spelar och loopar

# Namn och logga
pygame.display.set_caption("Space Invader")  # Namn
icon = pygame.image.load('Loga mitten.png')  # Logga
pygame.display.set_icon(icon)

# Spelare
playerImg = pygame.image.load('Bajen skepp.png')  # Spelarens skepp

score_value = 0  # poängens start värde
font = pygame.font.Font('freesansbold.ttf', 35)  # textens storlek och utseende

textX = 20  # textens X-cor
textY = 20  # textens Y-cor

lives_value = 10  # Antal liv vid start
live_font = pygame.font.Font('freesansbold.ttf', 35)  # textens storlek och utseende

heartX = 20  # textens X-cor
heartY = 50  # textens Y-cor

# ===================================================================================


# =============================================
# Spelarens kordinater
playerX = 370  # X-cor
playerY = 480  # Y-cor
playerX_change = 0

# Fiender, tomma listor
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10  # Antal fiender


for i in range(num_of_enemies):  # Går igenom antal fiender
    enemyImg.append(pygame.image.load('fiende.png'))  # Laddar fiende bilden
    enemyX.append(random.randint(0, 736))  # Spawn på X
    enemyY.append(random.randint(20, 101))  # Spawn på Y
    enemyX_change.append(4)
    enemyY_change.append(40)

# Ready = Kulan är utanför rutan
# Fire = kulan är i rutan


# Kulan
bulletImg = pygame.image.load('bullet2.png')  # Bild på kulan
bulletX = 0  # Hur kulan rör sig på X
bulletY = 480  # Hur kulan rör sig på Y
bulletX_change = 0  # Hastighet X
bulletY_change = 2  # Hastighet Y
bullet_state = 'ready'  # 'Ready' = Kulan är utanför rutan

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)  # används inte

# quit text
quit_font = pygame.font.Font('freesansbold.ttf', 30)  # Används inte


# Poäng function
def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 155, 0))  # Vad ska stå, vilken färg
    screen.blit(score, (x, y))  # trycker det på skärmen

# Liv funtion
def show_lives(x, y):
    lives = live_font.render('Lives : ' + str(lives_value), True,
                             (255, 0, 0))  # Vad ska stå, vilken färg
    screen.blit(lives, (x, y))  # Trycker det på skärmen


# Game over texten
def game_over_text():
    over_text = over_font.render('GAME OVER: ', True, (255, 0, 0))# Vad ska stå, vilken färg
    screen.blit(over_text, (200, 250))  # Trycker det på skärmen


# Quit texten (fungerar på samma sätt som poäng funktionen)
def quit_text():
    quit_text = quit_font.render('Quit to restart', True, (255, 255, 255))
    screen.blit(quit_text, (310, 400))

# Spelar functionen med X och Y som argument
def player(x, y):
    screen.blit(playerImg, (x, y))

# Fiende functionen med X, Y, I som argument
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"  # Fire = kulan syns i rutan
    screen.blit(bulletImg, (x + 16, y + 10))  # Visar kulan


# ===================================================================================
# Avgör om det sker kollisioner eller inte
def isCollision(enemyX, enemyY, bulletX, bulletY):  # Kontrollerar om fiende och kulan kolliderar
    x = enemyX - bulletX  # Matte för distans beräkning
    y = enemyY - bulletY  # Matte för distans beräkning
    distance = math.sqrt(x * x + y * y)  # Distans formel
    if distance < 27:  # Om distansen är mer än 27 är kollision falskt och annars är det sant
        # print(distance)
        return True  # Sant
    else:
        return False  # Falskt


# Spel loop
running = True  # Kör = sant
while running:  # while loop

    # RGB = Röd, Grön, blå
    screen.fill((0, 0, 0))
    # Bakgrund bild
    screen.blit(background, (0, 0))
    for event in pygame.event.get():  # For loop
        if event.type == pygame.QUIT:
            running = False  # Kör är = falskt

        # ===========================================
        # Minskar hastigheten på kulorna beroende på poäng
        if score_value >= 10000:  # På 10 000 poäng
            bulletY_change -= 0.1  # Minus 0.1 på hastigheten (startar på 2)


        if score_value >= 20000:  # På 20 000 poäng osv
            bulletY_change -= 0.1


        if score_value >= 30000:
            bulletY_change -= 0.1


        if score_value >= 100000:
            bulletY_change = 1

        # ===========================================



        # Kollar vilken pil knapp som trycks ned
        if event.type == pygame.KEYDOWN:  # Om en tangent trycks ned så...
            if event.key == pygame.K_LEFT:  # Om vänster pilen
                playerX_change = -1
            if event.key == pygame.K_RIGHT:  # Om höger pilen
                playerX_change = 1
            if event.key == pygame.K_SPACE:  # Om space
                if bullet_state is "ready":  # Om bullet_state = ready så händer...
                    bullet_sound = mixer.Sound('bullet sound2.mp3')  # Ljudet av kulan
                    bullet_sound.play()  # Spelar ljudet av kulan en gång
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # Om tangeten släpps
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # Förändringen i X är lika med  0



    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Fiendens rörelse

    for i in range(num_of_enemies):  # Kollar igenom alla fiender

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:  # om fienden x-cor är => 0...
            enemyX_change[i] = 0.5  # Så åker den med 0.5 hastighet åt höger
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:   # om fienden x-cor är => 736...
            enemyX_change[i] = -0.5  # Så åker den med -0.5 hastighet åt vänster
            enemyY[i] += enemyY_change[i]

        # Kollision spelare
        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)  # Kollar efter kolitioner mellan spelaren och fienden
        if collision:  # Om kolision mellan fiende och kula...
            lives_value -= 1  # Minus ett liv
            if lives_value <= 0:  # Om liv är <= 0...
                time.sleep(5)  # Frys i 5 sekunder
                #quit_text()
                bullet_state = 'ready'  # Ändra bullet_state från fire till ready
                score_value = 0  # Ändra poäng till 0
                lives_value = 10  # Antal start liv 10
                #enemyX[i] = random.randint(0, 736)
                #enemyY[i] = random.randint(50, 150)

        # Kollition kula fiende
        if collision == False:  # Om kolission = false
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            explosion_sound = mixer.Sound('explosion.mp3')
            explosion_sound.play()

            if bulletY < 480:
                score_value += 10
                print(score_value, "score")

            bulletY = 480
            bullet_state = "ready"

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Kulans rörelse
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    show_lives(heartX, heartY)
    pygame.display.update()
