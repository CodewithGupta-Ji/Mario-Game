"""
Hii, i am Prathamesh Gupta,
I programe this game in 12/7/2020
"""

import pygame
import random
from pygame import mixer


pygame.init()
mixer.init()
music3 = mixer.music

game_width = 1000
game_height = 650

# Creating window
gameWindow = pygame.display.set_mode((game_width,game_height))  # add full screen at end
pygame.display.set_caption("Mario Game")

# Images
introimg = pygame.image.load("Images\Start.png")
introimg = pygame.transform.scale(introimg,(game_width,game_height)).convert_alpha()

clock = pygame.time.Clock()


def Introscreen():
    exit = True
    playmusic('sounds\mario_theme.wav')
    while exit:
        gameWindow.blit(introimg, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False

            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_h:
                    gameloop()
                    exit = False


font = pygame.font.SysFont("Forte", 20)
def plot_text(text,color,x,y):
    screen_font = font.render(text, True,color)
    gameWindow.blit(screen_font, [x, y])

def gameloop():
    # Game images
    cactusimg = pygame.image.load("Images\cactus_withBreaks.png")
    cactusimg_rect = cactusimg.get_rect()
    cactusimg_rect.left = 0
    fireimg = pygame.image.load("Images\Fire_bricks.png")
    fireimg_rect = fireimg.get_rect()
    fireimg_rect.left = 0
    dragonimg = pygame.image.load("Images\Dragon.png")
    dragonimg_rect = dragonimg.get_rect()
    dragonimg_rect.left = 0
    marioimg = pygame.image.load("Images\Mario.png")
    marioimg_rect = marioimg.get_rect()
    marioimg_rect.left = 0
    Fireballimg = pygame.image.load("Images\Fireball.png").convert_alpha()
    Fireballimg_rect = Fireballimg.get_rect()
    Fireballimg_rect.left = 0
    playmusic('sounds\mario_theme.wav')

    # Game Variables
    exit =True
    mario_velocity = 350
    velocity_up = 0
    velocity_down = 0
    dragon_velocity_up = 0
    dragon_velocity_down = 2
    dragon_posi = 100
    ball_posi_x = []
    ball_posi_y = []
    ball_produce = 5
    score = 0
    white = (255,255,255)

    with open("sounds\mario_highScore.txt","r") as f:
        high_score = f.read()

    while exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    velocity_up= 5
                if event.key == pygame.K_DOWN:
                    velocity_down= 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    velocity_up=0
                if event.key == pygame.K_DOWN:
                    velocity_down =0

        dragon_posi-=dragon_velocity_up
        dragon_posi+=dragon_velocity_down
        mario_velocity-=velocity_up
        mario_velocity+=velocity_down

        # Dragon up and down Controls
        if dragon_posi<=80:
            dragon_velocity_up=0
            dragon_velocity_down=2
        if dragon_posi>=500:
            dragon_velocity_down=0
            dragon_velocity_up=2

        # game out statement by obstecals
        if mario_velocity<75 or mario_velocity>525:
            game_over(high_score,score)
            exit = False

        gameWindow.fill((0, 0, 0))
        gameWindow.blit(dragonimg, (900, dragon_posi))
        gameWindow.blit(cactusimg, (0, -125))
        gameWindow.blit(fireimg, (0, 580))
        plot_text(f"Score : {score}",white,200,80)
        plot_text(f"Highest Score : {high_score}",white,600,80)
        gameWindow.blit(marioimg, (5, mario_velocity))
        pygame.display.update()


        # fire ball system
        if len(ball_posi_y)<ball_produce:
            ball_posi_y.append(random.randint(50,650))
            ball_posi_x.append(850)

        for i in range(len(ball_posi_y)-1):
            if ball_posi_x[i] < 2:
                ball_posi_y.pop(i)
                ball_posi_x.pop(i)
                score+=1

        for i in range(len(ball_posi_y)):
            if abs(dragon_posi+5)  >= ball_posi_y[i]:
                gameWindow.blit(Fireballimg, (ball_posi_x[i], ball_posi_y[i]))
                pygame.display.update()
                ball_posi_x[i] = ball_posi_x[i] - 3

        for i in range(len(ball_posi_y)):
            if abs(ball_posi_x[i]-3)<40 and abs(ball_posi_y[i]-mario_velocity)<50:
                ball_posi_x.pop(i)
                ball_posi_y.pop(i)
                game_over(high_score,score)

        clock.tick(90)

    pygame.quit()
    quit()

def playmusic(songname):
    music3.load(songname)
    music3.play()

def game_over(high_score,score):
    exit = True
    backgroung_img = pygame.image.load("Images\end.png")
    backgroung_img = pygame.transform.scale(backgroung_img, (game_width, game_height)).convert_alpha()

    playmusic("sounds\mario_dies.wav")
    if int(high_score)<score:
        with open("sounds\mario_highScore.txt", "w") as f:
            f.write(str(score))

    while exit:
        gameWindow.blit(backgroung_img, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = False

            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_ESCAPE:
                    gameloop()
                    exit = False
                else:
                    exit = False

Introscreen()