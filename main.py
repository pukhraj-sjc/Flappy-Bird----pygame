#!/usr/bin/python
"""
Owner: Pukhraj-sjc
Description: Flappy bird game
"""
# Standard Modules
import random
import sys
import pygame
from pygame.locals import *

# variables
FPS = 32
WIDTH = 289
HEIGHT = 511
GROUNDY = HEIGHT * 0.8
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
images = {}
sounds = {}
PLAYER = 'gallery/gameimages/bird.png'
BACKGROUND = 'gallery/gameimages/background.png'
PIPE = 'gallery/gameimages/pipe.png'


def turnOn():
    """
    shows the welcome images on the screen
    :return:
    """
    playerx = int(WIDTH / 5)
    playery = int((HEIGHT - images['player'].get_height()) / 2)
    messagey = int(WIDTH * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(images['background'], (0, 0))
                SCREEN.blit(images['player'], (playerx, playery))
                SCREEN.blit(images['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def startGame():
    """
    This function handles the logic after the welcome screen
    :return:
    """
    score = 0
    playerx = int(WIDTH / 5)
    playery = int(WIDTH / 5)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': WIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': WIDTH + 200 + (WIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': WIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': WIDTH + 200 + (WIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8  # velocity while flapping
    playerFlapped = False  # It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    sounds['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)  # This function will return true if the player is crashed
        if crashTest:
            return

            # check for score
        playerMidPos = playerx + images['player'].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + images['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                sounds['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = images['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -images['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets blit our gameimages now
        SCREEN.blit(images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(images['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(images['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(images['base'], (basex, GROUNDY))
        SCREEN.blit(images['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += images['numbers'][digit].get_width()
        Xoffset = (WIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(images['numbers'][digit], (Xoffset, HEIGHT * 0.12))
            Xoffset += images['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        sounds['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = images['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < images['pipe'][0].get_width()):
            sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + images['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < \
                images['pipe'][0].get_width():
            sounds['hit'].play()

            return True

    return False

def getRandomPipe():
    """
    generate position of two pipes for bliting on the screen
    :return:
    """

    pipeHeight = images['pipe'][0].get_height()
    offset = HEIGHT / 3
    y2 = offset + random.randrange(0, int(HEIGHT - images['base'].get_height() - 1.2 * offset))
    pipeX = WIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # Upper Pipe
        {'x': pipeX, 'y': y2}  # Lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption(('Flappy Bird by Pukhraj'))
    images['numbers'] = (
        pygame.image.load('./gallery/gameimages/0.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/1.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/2.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/3.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/4.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/5.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/6.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/7.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/8.png').convert_alpha(),
        pygame.image.load('./gallery/gameimages/9.png').convert_alpha(),
    )

    images['base'] = pygame.image.load('./gallery/gameimages/base.png').convert_alpha()
    images['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    sounds['die'] = pygame.mixer.Sound('./gallery/gamesounds/die.wav')
    sounds['hit'] = pygame.mixer.Sound('./gallery/gamesounds/hit.wav')
    sounds['point'] = pygame.mixer.Sound('./gallery/gamesounds/point.wav')
    sounds['swoosh'] = pygame.mixer.Sound('./gallery/gamesounds/swoosh.wav')
    sounds['wing'] = pygame.mixer.Sound('./gallery/gamesounds/wing.wav')

    images['background'] = pygame.image.load(BACKGROUND).convert()
    images['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        turnOn()
        startGame()
