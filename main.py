import pygame
from pygame.locals import *
import random

pygame.init()
display_width = 400
display_height = 400
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
background = pygame.image.load("sky.png")
pygame.display.set_caption("Flappy Bird")
bird = pygame.image.load("bird.png")
pipe = pygame.image.load("pipe.png")

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
smallfont = pygame.font.Font("freesansbold.ttf",20)
medfont = pygame.font.Font("freesansbold.ttf",30)
largefont = pygame.font.Font("freesansbold.ttf",50)

def text_objects(text, color, size):
    if (size == "small"):
        textSurface = smallfont.render(text, True, color)
    elif (size == "medium"):
        textSurface = medfont.render(text, True, color)
    elif (size == "large"):
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = int(display_width/2),int(display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def pause(score):
    paused = True
    message_to_screen("Game Over", red, -50, "large")
    message_to_screen("Score "+str(score), green, 0, "medium")
    message_to_screen("Press r to restart the game", black, 25, "small")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_r):
                    game_loop()
        
        clock.tick(5)


def show_score(x,y,score_value,color):
    score = smallfont.render("Score: "+str(score_value),True,color)
    gameDisplay.blit(score, (x,y))

def isCollide(player_x,player_y,pipe_coordinate):
    if (player_y < 0 or player_y > display_height-bird.get_height()):
        return True
    if (pipe_coordinate[0][0] < player_x+bird.get_width() < pipe_coordinate[0][0]+pipe.get_width() and (player_y < pipe_coordinate[0][2]+pipe.get_height() or player_y+bird.get_height() > pipe_coordinate[0][1])):
        return True
    return False

def get_random_pipe():
    pipe_height = pipe.get_height()
    offset = 125
    x = display_width
    y1 = offset+random.randrange(offset,display_height-offset)
    y2 = y1-offset-pipe_height
    return [x,y1,y2]

def game_loop():
    score = 0
    player_x = int(display_width/5)
    player_y = int(display_height/2)
    player_y_change = 6
    player_flapped = False
    upper_pipe = pygame.transform.rotate(pipe,180)
    lower_pipe = pipe
    pipe_coordinate = []
    pipe_coordinate.append(get_random_pipe()) 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_flapped = True
                    player_y_change = -12
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player_flapped = False
                    player_y_change = 6

        gameDisplay.fill(white)
        gameDisplay.blit(background, (0,0))
        player_y += player_y_change
        gameDisplay.blit(bird,(player_x,player_y))

        pipe_coordinate[0][0] -= 10
        gameDisplay.blit(lower_pipe,(pipe_coordinate[0][0],pipe_coordinate[0][1]))
        gameDisplay.blit(upper_pipe,(pipe_coordinate[0][0],pipe_coordinate[0][2]))
        if (pipe_coordinate[0][0]-pipe.get_width()-10 < 0):
            del pipe_coordinate[0]
            pipe_coordinate.append(get_random_pipe())
            gameDisplay.blit(lower_pipe,(pipe_coordinate[0][0],pipe_coordinate[0][1]))
            gameDisplay.blit(upper_pipe,(pipe_coordinate[0][0],pipe_coordinate[0][2]))

        crash = isCollide(player_x,player_y,pipe_coordinate)
        if crash:
            pause(score)
        if (pipe_coordinate[0][0] < player_x < pipe_coordinate[0][0]+pipe.get_width() and pipe_coordinate[0][2]+pipe.get_height() < player_y < pipe_coordinate[0][1]-bird.get_height()):
            score += 1
        
        show_score(10,10,score,black)
        pygame.display.update()
        clock.tick(20)

game_loop()
pygame.quit()
quit()
